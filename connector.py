import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import pdist, squareform
import pandas as pd

my_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "zabatly"
)

def recommend(userData):
    
    cursor = my_db.cursor()
    list_of_visited_venues = []
    
    if type(userData) is int:
        sql_user = "SELECT * FROM visited_venues WHERE userID = %s"
        userID = userData
        cursor.execute(sql_user,(userID,))
        user_record = cursor.fetchall()
    
        if len(user_record) == 0:
            return {}
        else:
            venueID = [item[1] for item in user_record]
            sql = 'SELECT name FROM venues WHERE id in ({})'.format(', '.join('%s' for i in venueID))
            cursor.execute(sql,venueID)
            venue_data = cursor.fetchall()
            
            for item in venue_data:
                list_of_visited_venues.append(item[0])
    else:
        
        list_of_visited_venues.append(userData)

    #recommender process
    venues_statement = "SELECT * FROM venues"
    cursor.execute(venues_statement)
    venues = cursor.fetchall()

    #load the data into a dataframe
    df = pd.DataFrame(venues, columns=['VenueID', 'VenueName', 'VenueArab', 'CategoryID', 'CityID', 'Capacity', 'Description', 'arDescription', 'Rating', 'Price', 'Space', 'rules', 'arRules', 'Policy', 'arPolicy', 'HostID'])

    print(df)

    #category_cross_tab
    category_cross_tab = pd.crosstab(df['VenueName'], df['CategoryID'])
    city_cross_tab = pd.crosstab(df['VenueName'], df['CityID'])

    #jaccard distances
    category_jaccard_distances = pdist(category_cross_tab.values,metric = 'jaccard')
    city_jaccard_distances = pdist(city_cross_tab.values,metric = 'jaccard')

    #square form
    category_square_jaccard_distances = squareform(category_jaccard_distances)
    city_square_jaccard_distances = squareform(city_jaccard_distances)

    #jaccard similarity
    category_jaccard_similarity = 1 - category_square_jaccard_distances
    city_jaccard_similarity = 1 - city_square_jaccard_distances

    #category based and city based dataframes
    category_based_df = pd.DataFrame(category_jaccard_similarity, index = category_cross_tab.index, columns = category_cross_tab.index)
    city_based_df = pd.DataFrame(city_jaccard_similarity, index = city_cross_tab.index, columns = city_cross_tab.index) 

    #category based
    user_visited_category = category_based_df.reindex(list_of_visited_venues)
    user_prof_category = user_visited_category.max()

    #city based
    user_visited_city = city_based_df.reindex(list_of_visited_venues)
    user_prof_city = user_visited_city.max()
    user_prof = user_prof_category.combine(user_prof_city, max)

    #sort values
    user_prof.sort_values(ascending = False)

    #View similarity score
    user_prof = user_prof[~user_prof.index.isin(list_of_visited_venues)]
    user_prof = pd.DataFrame(user_prof.values, index = user_prof.index, columns = ["similarity score"])

    #recommendations
    category_recommendation = user_prof[user_prof['similarity score'] != 0]


    #text based filtering 
    #vectorizer object
    tfidvec = TfidfVectorizer(min_df = 2, max_df = 0.7)

    #fit transform
    vectorized_data = tfidvec.fit_transform(df["Description"])

    #create a dataframe
    tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns = tfidvec.get_feature_names_out(), index = df["VenueName"])
    print(tfidf_df)

    #compute the cosine similarity
    cosine_similarity_array = cosine_similarity(tfidf_df)

    #create a cosine similarity dataframe
    cosine_similarity_df = pd.DataFrame(cosine_similarity_array, columns = tfidf_df.index, index = tfidf_df.index)

    #re-index visited venues
    visited_venues = tfidf_df.reindex(list_of_visited_venues)

    #calculate user profile (preferrences)
    user_prof = visited_venues.mean()

    #create a dataframe for the unvisited venues
    not_visited = tfidf_df.drop(list_of_visited_venues, axis = 0)

    #compute cosine similarity for user data
    user_prof_similarities = cosine_similarity(user_prof.values.reshape(1,-1), not_visited)

    #user similarity dataframe
    user_prof_similarities_df = pd.DataFrame(user_prof_similarities.T, index = not_visited.index, columns = ["similarity score"])

    #sort values
    user_prof_similarities_df.sort_values(by = 'similarity score', inplace = True, ascending = False)

    #print(user_prof_similarities_df)

    #print(category_recommendation)

    user_prof_similarities_df = user_prof_similarities_df[user_prof_similarities_df["similarity score"] >= 0.2]
    #print(user_prof_similarities_df)

    final_df = user_prof_similarities_df.merge(category_recommendation, left_index=True, right_index=True)
    #print(final_df)
    
    venue_recommendation_list = final_df.index.to_list()
    #print(venue_recommendation_list)
    
    if len(venue_recommendation_list) < 3:
        large_df = user_prof_similarities_df[~user_prof_similarities_df.index.isin(venue_recommendation_list)]
    
        added_venues = large_df.index.to_list()
        print(added_venues)
    
        for added in added_venues:
            venue_recommendation_list.append(added)
        
    sql = 'SELECT id FROM venues WHERE name in ({})'.format(', '.join('%s' for i in venue_recommendation_list))
    cursor.execute(sql,venue_recommendation_list)
    venue_recommendation = cursor.fetchall()
    
    final_recommendation = [item for sublist in venue_recommendation for item in sublist]
    print(final_recommendation)
    
    return final_recommendation



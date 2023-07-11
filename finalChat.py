# %%
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers , activations , models , preprocessing , utils
import pandas as pd

# %%
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout

# %%
data_path1='chatbot dataset.txt'

# %%
input_texts = []
target_texts = []
with open(data_path1,'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
for line in lines:
    input_text = line.split('\t')[0]
    target_text = line.split('\t')[1]
    input_texts.append(input_text)
    target_texts.append(target_text)

# %%
print('type of input_text',type(input_text))
print('type of target_texts',type(target_texts))

# %%
##converting the list in pandas dataframe since input_text,target_text are both are type of list
zippedList =  list(zip(input_texts, target_texts))
lines = pd.DataFrame(zippedList, columns = ['input' , 'output']) 
lines.head()

# %%
input_lines = list()
for line in lines.input:
    input_lines.append( line ) 

tokenizer = preprocessing.text.Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n،؛؟«»،؛؟')
tokenizer.fit_on_texts( input_lines )
tokenized_text = tokenizer.texts_to_sequences(input_lines)
print(tokenized_text)

length_list = list()
for token_seq in tokenized_text:
    length_list.append( len( token_seq ))
max_input_length = np.array( length_list ).max()
print( 'Input max length is {}'.format( max_input_length ))

padded_input_lines = preprocessing.sequence.pad_sequences( tokenized_text , maxlen=max_input_length , padding='post' )
encoder_input_data = np.array( padded_input_lines )
print( 'Encoder input data shape -> {}'.format( encoder_input_data.shape ))

input_word_dict = tokenizer.word_index
num_input_tokens = len( input_word_dict )+1
print( 'Number of Input tokens = {}'.format( num_input_tokens))
print(input_word_dict)
print(padded_input_lines)
print(encoder_input_data)

# %%
output_lines = list()
for line in lines.output:
    output_lines.append( '<START> ' + line + ' <END>' )  

tokenizer = preprocessing.text.Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n،؛؟«»،؛؟')
tokenizer.fit_on_texts( output_lines ) 
tokenized_output_lines = tokenizer.texts_to_sequences( output_lines ) 

length_list = list()
for token_seq in tokenized_output_lines:
    length_list.append( len( token_seq ))
max_output_length = np.array( length_list ).max()
print( 'Output max length is {}'.format( max_output_length ))

padded_output_lines = preprocessing.sequence.pad_sequences( tokenized_output_lines , maxlen=max_output_length, padding='post' )
decoder_input_data = np.array( padded_output_lines )
print( 'Decoder input data shape -> {}'.format( decoder_input_data.shape ))

output_word_dict = tokenizer.word_index
num_output_tokens = len( output_word_dict )+1
print( 'Number of Output tokens = {}'.format( num_output_tokens))
print(output_lines)
print(decoder_input_data)

# %%
decoder_target_data = list()
for token_seq in tokenized_output_lines:
    decoder_target_data.append( token_seq[ 1 : ] )   
padded_output_lines = preprocessing.sequence.pad_sequences( decoder_target_data , maxlen=max_output_length, padding='post' )
onehot_output_lines = utils.to_categorical( padded_output_lines , num_output_tokens )
decoder_target_data = np.array(onehot_output_lines )
print(decoder_target_data)
print( 'Decoder target data shape -> {}'.format( decoder_target_data.shape ))

# %%
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout, Attention
from tensorflow.keras.models import Model

# %%
encoder_inputs = tf.keras.layers.Input(shape=( None , ))
encoder_embedding = tf.keras.layers.Embedding( num_input_tokens, 256 , mask_zero=True ) (encoder_inputs)
#mask_zero = true so that 0 in the padding sequence isn't weighted in our process
encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 256 , return_state=True , recurrent_dropout=0.2 , dropout=0.2 )( encoder_embedding )
encoder_states = [ state_h , state_c ]

decoder_inputs = tf.keras.layers.Input(shape=( None ,  ))
decoder_embedding = tf.keras.layers.Embedding( num_output_tokens, 256 , mask_zero=True) (decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM( 256 , return_state=True , return_sequences=True , recurrent_dropout=0.2 , dropout=0.2)
#return_sequence = true so that the output for each time step is returned 
decoder_outputs , _ , _ = decoder_lstm ( decoder_embedding , initial_state=encoder_states )
decoder_dense = tf.keras.layers.Dense( num_output_tokens , activation=tf.keras.activations.softmax ) 
output = decoder_dense ( decoder_outputs )

'''
model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output )
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# %%
model.summary()

# %%
utils.plot_model(model, to_file='model_summary.png', show_shapes=True)

# %%
model.fit([encoder_input_data , decoder_input_data], decoder_target_data, batch_size=32, epochs=100)
model.save( 'model.h5' )
'''
# %%
def make_inference_models():
    # Load your trained model
    model = tf.keras.models.load_model('final_model.h5')

    # Create new input layers for encoder and decoder inputs
    encoder_inputs = model.input[0]
    decoder_inputs = model.input[1]

    # Extract encoder layers and weights from the trained model
    encoder_embedding = model.get_layer('embedding')(encoder_inputs)
    encoder_lstm = model.get_layer('lstm')
    _, state_h, state_c = encoder_lstm(encoder_embedding)
    encoder_states = [state_h, state_c]
    encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

    # Extract decoder layers and weights from the trained model
    decoder_embedding = model.get_layer('embedding_1')(decoder_inputs)
    decoder_lstm = model.get_layer('lstm_1')
    decoder_dense = model.get_layer('dense')
    decoder_outputs, state_h, state_c = decoder_lstm(decoder_embedding, initial_state=encoder_states)
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_states = [state_h, state_c]
    decoder_model = tf.keras.models.Model([decoder_inputs] + encoder_states, [decoder_outputs] + decoder_states)

    return encoder_model, decoder_model


# %%
import tensorflow as tf
def str_to_tokens( sentence : str ):
    words = sentence.lower().split()
    tokens_list = list()
    for word in words:
        if word in input_word_dict:
            tokens_list.append( input_word_dict[ word ] ) 
    return preprocessing.sequence.pad_sequences( [tokens_list] , maxlen=max_input_length , padding='post')

# %%
enc_model , dec_model = make_inference_models()

def bot_conv(user_input):
         
        states_values = enc_model.predict(str_to_tokens(user_input) , verbose = 0)
        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = output_word_dict['start']
        stop_condition = False
        decoded_translation = ''
        
        while not stop_condition :
            dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + states_values , verbose = 0)
            sampled_word_index = np.argmax( dec_outputs[0, -1, :] )
            sampled_word = None
            for word , index in output_word_dict.items() :
                if sampled_word_index == index :
                    decoded_translation += ' {}'.format( word )
                    sampled_word = word
            
            if sampled_word == 'end' or len(decoded_translation.split()) > max_output_length:
                stop_condition = True
                
            empty_target_seq = np.zeros( ( 1 , 1 ) )  
            empty_target_seq[ 0 , 0 ] = sampled_word_index
            states_values = [ h , c ] 
        return decoded_translation.replace(' end', '')



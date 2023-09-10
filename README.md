<div align="center">
    <h1>Zabatly AI</h1>
    <p>Empowering Conversations, Tailoring Recommendations</p>
    <img src="./misc/showcase.gif" width="1000"/>
    <br>
    <a href="https://github.com/Zabatly/AI/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Zabatly/AI?style=for-the-badge" alt="license gpl-3.0"/>
    </a>
</div>

<details>
<summary style="font-size: 21px;">Table of Contents</summary>
<ol>
    <li><a href="#introduction">Introduction</a></li>
    <ul>
        <li><a href="#project-description">Project Description</a></li>
        <li><a href="#features">Features</a></li>
    </ul>
    <li><a href="#getting-started">Getting Started</a></li>
    <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
    </ul>
    <li><a href="#technologies">Technologies</a></li>
    <li><a href="#wishlist">Wishlist</a></li>
    <li><a href="#contributors">Contributors</a></li>
</details>
<br>

# Introduction

## Project Description

This project combines a support chatbot powered by a Seq2Seq model with a recommendation system built on content-based filtering. The chatbot assists users by providing real-time responses to their inquiries, while the recommendation system offers personalized suggestions based on user preferences and content analysis. Together, they enhance user engagement and satisfaction by delivering tailored assistance and relevant content.

## Features

- Multilingual Chatbot that seamlessly switches between Arabic and English.
- Real-time support for venue reservations and inquiries.
- Personalized venue recommendations based on user activities.
- Similar venue suggestions to enhance user exploration.

# Getting Started

## Prerequisites

- Python [v3.10.11+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/doc/mysql-getting-started/en/) with our [database design](https://github.com/Zabatly/AI/blob/main/misc/zabatly_data.sql)

## Installation

- Clone the github repo.

```bash
# Cloning our github repo.
git clone https://github.com/Zabatly/AI.git
```

- Create & activate python [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

- Install python packages

```bash
# Installing all required python packages from requirements.txt
pip install -r requirements.txt
```

- Run your MySQL database and make sure your details match the ones in [`app.py`](https://github.com/Zabatly/AI/blob/main/app.py)

```py
host = "localhost",
user = "root",
password = "",
database = "zabatly"
```

- Run the application and enjoy!

```bash
python -m flask run
```

- Check our [universal application](https://github.com/Zabatly/website) to interact with the chatbot.

# Technologies

The models and frameworks used in our project:

- TensorFlow
- scikit-learn
- Pandas & NumPy
- Flask
- MySQL

# Wishlist

- [ ] Increase the chatbot's dataset even further for both languages
- [ ] Enhance the chatbot's NLU capabilities to understand user intents and entities more accurately
- [ ] Expand multilingual support to include more languages to reach a wider user base.

# Contributors

Special thanks to the team for the help across the board

- [Youssef Elmarakshy](https://github.com/Carbowix)
- [Taha Hesham](https://github.com/tahahesham)
- [Mostafa Awara](https://github.com/mostafavic)
- [Mohammed Effat](https://github.com/bondo2boy)

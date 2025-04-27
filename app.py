import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

if not os.path.exists('similarity.pkl'):
    with st.spinner('Downloading recommendation model (first run only)...'):
        file_id = '1bIpLLPGhqiGXO7blFFAIntM1o__2YInh'
        url = f'https://drive.google.com/uc?id={'1bIpLLPGhqiGXO7blFFAIntM1o__2YInh'}'
        gdown.download(url, 'similarity.pkl', quiet=False)


# Load data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Create a list of movie titles for the dropdown
movie_titles = movies_df['title'].values

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d70d20613fd134fb32f9d0431dd166a3&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster =[]
    for i in similar_movies:
        movie_id = movies_df.iloc[i[0]].movie_id
        # fetching poster using API from TMDB
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)

    return recommended_movies , recommended_movies_poster


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the movie you like!',
    movie_titles
)

if st.button('Recommend'):
    name,poster= recommend(selected_movie_name)
    col1, col2, col3 , col4 , col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col4:
        st.text(name[4])
        st.image(poster[4])
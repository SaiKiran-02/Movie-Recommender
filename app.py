import streamlit as st
import pickle
import pandas as pd
import requests

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .movie-title {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        text-align: center;
        height: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #E03131;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .stImage:hover {
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="main-header">🎬 Movie Recommender System</div>', unsafe_allow_html=True)


# Load data
@st.cache_resource
def load_data():
    movies_df = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies_df, similarity


movies_df, similarity = load_data()

# Create a list of movie titles for the dropdown
movie_titles = movies_df['title'].values


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d70d20613fd134fb32f9d0431dd166a3&language=en-US')
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in similar_movies:
        movie_id = movies_df.iloc[i[0]].movie_id
        # fetching poster using API from TMDB
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)

    return recommended_movies, recommended_movies_poster


# Input section without white container
with st.container():
    st.markdown('<div class="subheader">Find Your Next Favorite Movie</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_movie_name = st.selectbox(
            'Select a movie you enjoyed:',
            movie_titles,
            index=0,
            help="Choose a movie you liked, and we'll recommend similar ones!"
        )

    with col2:
        recommend_button = st.button('Get Recommendations')

# Show recommendations
if recommend_button:
    with st.spinner('Finding similar movies for you...'):
        name, poster = recommend(selected_movie_name)

    st.markdown(f'<div class="subheader">Because you liked "{selected_movie_name}", you might enjoy:</div>',
                unsafe_allow_html=True)

    # Display recommendations in a grid
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f'<div class="movie-title">{name[i]}</div>', unsafe_allow_html=True)
            st.image(poster[i], use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #555; font-size: 0.8rem;">
    Powered by TMDB API | Movie data provided by The Movie Database
</div>
""", unsafe_allow_html=True)
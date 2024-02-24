import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

API_KEY=st.secrets["key"]
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def fetch_poster(movie_name):
    search_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"

    response = requests.get(search_url)
    data = response.json()

    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        return "No poster found for this movie"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:5]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)

        # fetch the movie poster
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))
    # return recommended_movie_names
    return recommended_movie_names,recommended_movie_posters



# Specify the path to your compressed pickle file
file_path = 'similarity.pkl.gz'

# Open the compressed file and decompress it
with gzip.open(file_path, 'rb') as f:
    # Load the data using pickle
    similarity = pickle.load(f)

movies=pd.read_csv('movies1.csv')
# movies = pickle.load(open('movies.pkl','rb'))

movies_list = movies['title'].values

# similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendor System')

option = st.selectbox(
    'Search Movies by Name',
    movies_list)

# st.button("Reset", type="primary")
if st.button('Recommend'):
    names,posters=recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)#beta_columns to columns
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

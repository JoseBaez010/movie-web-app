import streamlit as st
import requests
import pandas as pd

background_color = "linear-gradient(180deg, #6E48AA, #B538FF)"

st.markdown("<h1 style='text-align: center; color: black;'>Cinema Lit</h1>", unsafe_allow_html=True)

api_key = "bdb0d72516db605476b9d810383f277e"

option = st.sidebar.selectbox("Here are the other options: ", ("Main Page", "Movie Search", "Movie Statistics"))

if option == "Main Page":
    st.title("Home Page")

elif option == "Movie Search":
    st.title("Movie Search App")

    # Define the search parameters
    search_query = st.text_input("Enter movie title")
    movie_genre = st.multiselect("Select genre",
                                 ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama",
                                  "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
                                  "Science Fiction", "TV Movie", "Thriller", "War", "Western"])
    year_range = st.slider("Select release year range", 1900, 2023, (1950, 2023))

    # Make API request
    if st.button("Search"):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={search_query}"
        response = requests.get(url).json()

        # Filter movies based on release year range
        filtered_movies = [movie for movie in response['results'] if
                           year_range[0] <= int(movie['release_date'][:4]) <= year_range[1]]

        # Filter movies based on genre(s)
        if movie_genre:
            genre_id_dict = {"Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35, "Crime": 80,
                             "Documentary": 99,
                             "Drama": 18, "Family": 10751, "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
                             "Mystery": 9648, "Romance": 10749, "Science Fiction": 878, "TV Movie": 10770,
                             "Thriller": 53, "War": 10752, "Western": 37}

            filtered_movies = [movie for movie in filtered_movies if
                               any(genre_id == genre_id_dict[genre] for genre_id in movie["genre_ids"] for genre in
                                   movie_genre)]

        # Display filtered movie results
        for movie in filtered_movies:
            st.write(movie["title"])
            st.write(movie["overview"])
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.write(f"Rating: {movie['vote_average']}")
            st.write("---")
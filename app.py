import streamlit as st
import requests
import pandas as pd
import json
import numpy as np

background_color = "linear-gradient(180deg, #6E48AA, #B538FF)"
#5fa1e8 <- nice color to use as a theme
st.markdown("<h1 style='text-align: center; color: black;'>Cinema Fanatic</h1>", unsafe_allow_html=True)
st.divider()
api_key = "bdb0d72516db605476b9d810383f277e"
places_api_key = "AIzaSyA0Ci-gyYa06Bswegp0Iub5ZiS0iVApK_U"

option = st.sidebar.selectbox("Explore the web app: ", ("Home", "Search your Favorites", "Top-rated Data"))

# Home Page
if option == "Home":
    st.header("Welcome to :blue[Cinema Fanatic], a place where movie enthusiasts get their crave on")
    st.divider()
    st.text("Cinema Fanatic aims to provide users access to data related to Top-Rated movies.\nOn top of that, users "
            "can explore different genres and find any movie \nfrom a certain year!")
    st.divider()
    st.text("Try it out!")

    # Make api request
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    movies = data["results"]

    # Create button to get recently released movies
    if st.button("Recently Released Movies"):
        table_data = []
        for movie in movies:
            table_data.append([movie["title"], movie["release_date"], movie["vote_average"]])
        st.table(table_data)

    st.divider()

    # Section for finding the nearest Movie Theater
    st.title("Find your Nearest Movie Theater")
    zip_code = st.text_input("Enter your 5-digit zip code:")

    # Check valid zipcode
    if len(zip_code) != 5 or not zip_code.isdigit():
        st.warning("Please enter a valid 5-digit zip code.")
    else:
        # Api request for geocoding to get coordinates of zipcode
        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={places_api_key}")
        response_json = response.json()
        lat = response_json['results'][0]['geometry']['location']['lat']
        lng = response_json['results'][0]['geometry']['location']['lng']

        # Using this api request to find the nearby theaters
        radius = 80000  # set radius to 50 miles
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=movie_theater&key={places_api_key}"
        response = requests.get(url)
        response_json = response.json()

        # Making the map
        theaters = []
        for result in response_json['results']:
            theater = {
                'lat': result['geometry']['location']['lat'],
                'lon': result['geometry']['location']['lng']
            }
            theaters.append(theater)
        theaters_df = pd.DataFrame(theaters)
        theaters_df['LAT'] = theaters_df['lat']
        theaters_df['LON'] = theaters_df['lon']
        st.map(theaters_df[['LAT', 'LON']])

# Search
elif option == "Search your Favorites":
     # Make API request
    st.title("Movie Search")

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
                           movie['release_date'] and year_range[0] <= int(movie['release_date'].split("-")[0]) <=
                           year_range[1]]

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
        if filtered_movies:
            st.success("Movies are found here")
            for movie in filtered_movies:
                st.write(movie["title"])
                st.write(movie["overview"])
                st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
                st.write(f"Rating: {movie['vote_average']}")
                st.divider()
        else:
            st.error("Movies are not found here.")

elif option == "Top-rated Data":
    st.header("Top Rated Movies of All Time")

    # Make an API request
    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}'
    response = requests.get(url)

    # Data table with Top-rated movies
    top_rated_movies = response.json()['results']
    df = pd.DataFrame(top_rated_movies)
    show_columns = ['title', 'overview', 'popularity', 'release_date', 'vote_average', 'vote_count']
    df = df[show_columns]
    st.dataframe(df)

    # Options to display data
    st.subheader("Choose a method to display popularity data")
    display_line_chart = st.checkbox("Line chart")
    display_bar_chart = st.checkbox("Bar chart")

    # Code for the LineChart
    if display_line_chart:
        df = pd.DataFrame(top_rated_movies)
        df['release_date'] = pd.to_datetime(df['release_date'])
        df.set_index('release_date', inplace=True)
        chart_data = pd.DataFrame({'Popularity': df['popularity'], 'Release Date': df.index})
        st.line_chart(chart_data, use_container_width=True, x='Release Date', y='Popularity')
        st.caption("This chart shows the popularity of top rated movies over time.")

    # Code for the Bar Chart
    if display_bar_chart:
        df = pd.DataFrame(top_rated_movies)
        df['release_year'] = pd.DatetimeIndex(df['release_date']).year
        grouped = df.groupby('release_year')['popularity'].mean()
        chart_data = pd.DataFrame({'Release Year': grouped.index, 'Mean Popularity': grouped.values})
        chart_data = chart_data.sort_values(by='Release Year')
        st.bar_chart(chart_data, x='Release Year', y='Mean Popularity', use_container_width=True)
        st.caption('This chart shows the average popularity of top rated movies by release year.')
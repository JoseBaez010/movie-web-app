import streamlit as st
import requests
import pandas as pd

# Testing something out
# comment test
background_color = "linear-gradient(180deg, #6E48AA, #B538FF)"

st.markdown("<h1 style='text-align: center; color: black;'>Cinema Lit</h1>", unsafe_allow_html=True)


api_key = "bdb0d72516db605476b9d810383f277e"
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=en-US&page=1"

# Fetch the list of top-rated movies from the TMDB API
response = requests.get(url)
data = response.json()
movies = data["results"]
df = pd.DataFrame(movies)

# Calculate the number of rows and columns needed for the grid
num_cols = 5
num_rows = (len(movies) + num_cols - 1) // num_cols

# Create a list of empty lists to hold the movie posters for each column
poster_cols = [[] for _ in range(num_cols)]

# Loop through the list of movies and add their posters to the appropriate column
for i, movie in enumerate(movies):
    # Retrieve the URL for the poster image of the movie
    poster_path = movie["poster_path"]
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"

    # Add the poster URL to the appropriate column
    poster_cols[i % num_cols].append(poster_url)

# Display the posters in a grid of 5 columns and 5 rows
for row_idx in range(num_rows):
    # Create a list of columns for this row
    row_cols = st.columns(num_cols)

    # Loop through the columns and display the posters
    for col_idx in range(num_cols):
        poster_idx = row_idx * num_cols + col_idx
        if poster_idx < len(movies):
            row_cols[col_idx].image(poster_cols[col_idx][row_idx],
                                    caption=movies[poster_idx]["title"],
                                    use_column_width=True)

# Display the data in a table
table = st.dataframe(df)


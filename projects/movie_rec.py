
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

# Load the data and model
movies_dict = pickle.load(open("E:/NN_Projects/All_In_One/projects/model_controllers/movie/movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("E:/NN_Projects/All_In_One/projects/model_controllers/movie/similarity.pkl", "rb"))


def recommand(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

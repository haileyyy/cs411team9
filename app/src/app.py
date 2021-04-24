from flask import Flask, request, render_template
from imdb import get_imdb_movie
from watchmode import *

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/test',methods=['GET'])
def test():
    return "hello world!"

@app.route('/search',methods=['POST'])
def submit():
    request_data = request.form
    movie_list = get_imdb_movie(request_data['title'])
    return render_template('./info_page.html', movie_list=movie_list)

@app.route('/movie_info', methods=['POST'])
def movie_submit():
    request_data = request.form
    tmdb_ID = tmdbID_from_imdbID(request_data['imdb_id'])
    sources = sources_from_tmdbID(tmdb_ID)
    return render_template('./movie_info.html', movie_sources=sources)

@app.route('/new_user', methods=['GET', 'POST'])
def genre_submit():
    request_data = request.form
    genres = get_genres()
    scores = [0] * len(genres)
    movies = movies_from_genres(genres,3)
    display_movies = initial_movie_display(movies)
    return render_template('./new_user_genres.html', movietitles = get_names_from_movies(display_movies))

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')

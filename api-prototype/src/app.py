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
    watchmode_ID = watchmodeID_from_imdbID(request_data['imdb_id'])
    watchmode_Sources = sources_from_watchmodeID(watchmode_ID)
    sources = known_sources(watchmode_Sources)
    return render_template('./movie_info.html', movie_sources=sources)
    

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')

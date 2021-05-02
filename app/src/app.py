from flask import Flask, request, render_template
from imdb import get_imdb_movie
from watchmode import *
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder="templates")
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cai12345'
app.config['MYSQL_DATABASE_DB'] = 'userInfo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


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
    print(movie_list)
    return render_template('./info_page.html', movie_list=movie_list)

@app.route('/movie_info', methods=['POST'])
def movie_submit():
    request_data = request.form
    tmdb_ID = tmdbID_from_imdbID(request_data['imdb_id'])
    sources = sources_from_tmdbID(tmdb_ID)
    return render_template('./movie_info.html', movie_sources=sources)

@app.route('/new_user', methods=['GET', 'POST'])
def genre_submit():
    display_movies = initial_movie_display()
    return render_template('./new_user_genres.html', movietitles = display_movies)


@app.route('/new_user_sources', methods = ['GET','POST'])
def new_user_sources_submit():
    request_data = request.form
    services=[]
    cursor.execute("SELECT * FROM service")
    rows=cursor.fetchall()
    for row in rows:
        services.append(row[1])
    print(rows)
    services = ['Netflix','Hulu', 'HBO Max']
    return render_template('./new_user_sources.html',streaming_services=services)

@app.route('/update_user_service', methods = ['GET','POST'])
def update_user_service():
    request_data = request.form.getlist("s")
    print(request_data)
    return render_template('./results.html')

@app.route('/results', methods = ['GET','POST'])
def user_submit():
    request_data = request.form.getlist("m")
    genrescores = clean_genres(request_data)
    genres = get_genres()
    userscore = {}
    for genre in genres:
       userscore[genre[0]] = 5
    new_userscores = update_userscores(userscore,genrescores)
    return render_template('./results.html', resultList = request_data)

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')

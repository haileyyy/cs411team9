from secrets import SECRETS
from watchmode import *

from flask import Flask, redirect, url_for, render_template, make_response, request
from flask_dance.contrib.google import make_google_blueprint, google
from flaskext.mysql import MySQL
import os

app = Flask(__name__, template_folder="templates")

# Ignore that connection is not HTTPS (for local testing)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Setup Google OAuth
app.secret_key = SECRETS['flask_secret_key']
app.config['GOOGLE_OAUTH_CLIENT_ID'] = SECRETS['google_client_id']
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = SECRETS['google_client_secret']

google_bp = make_google_blueprint(scope=['email'], offline=True)
app.register_blueprint(google_bp, url_prefix='/login')

# Setup MySQL database connection settings
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = SECRETS['db-username']
app.config['MYSQL_DATABASE_PASSWORD'] = SECRETS['db-password']
app.config['MYSQL_DATABASE_DB'] = 'movierecommendation'
app.config['MYSQL_DATABASE_HOST'] = SECRETS['db-endpoint']
mysql.init_app(app)

# Initalize connection to MySQL database
conn = mysql.connect()
cursor = conn.cursor()

def isEmailUnique(email):
    cursor = conn.cursor()
    if cursor.execute('SELECT email FROM user WHERE email = "{0}"'.format(email)):
        return False
    else:
        return True

@app.route('/')
def index():
    if request.cookies.get('user_ID', None):
        return render_template('home.html')
    elif google.authorized:
        google_resp = google.get('/oauth2/v1/userinfo')
        assert google_resp.ok, google_resp.text
        del google_bp.token

        email = google_resp.json()['email']

        if isEmailUnique(email) == True:
            cursor.execute('INSERT INTO user (email) VALUES ("{}")'.format(email))
            conn.commit()

        cursor.execute('SELECT user_ID FROM user WHERE email="{}"'.format(email))
        for x in cursor:
            user_ID = x[0]

        resp = make_response(render_template('home.html'))
        resp.set_cookie('user_ID', str(user_ID))

        return resp
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout')
def logout():
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('user_ID', '', expires=0)
    return resp

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
    app.debug = True
    app.run(host='0.0.0.0')

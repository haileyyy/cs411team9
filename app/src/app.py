from secrets import SECRETS
from watchmode import *

from flask import Flask, redirect, url_for, render_template, make_response, request
from flask_dance.contrib.google import make_google_blueprint, google
from flaskext.mysql import MySQL
import os, base64

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
    if cursor.execute('SELECT email FROM user WHERE email = "{0}"'.format(email)):
        return False
    else:
        return True

@app.route('/')
def index():
    if request.cookies.get('user_id', None):
        return redirect('/home')
    elif google.authorized:
        google_resp = google.get('/oauth2/v1/userinfo')
        assert google_resp.ok, google_resp.text
        del google_bp.token

        email = google_resp.json()['email']

        if isEmailUnique(email) == True:
            cursor.execute('INSERT INTO user (email) VALUES ("{}")'.format(email))
            conn.commit()

        cursor.execute('SELECT user_id FROM user WHERE email="{}"'.format(email))
        for x in cursor:
            user_id = x[0]

        resp = make_response(redirect('/home'))
        resp.set_cookie('user_id', str(user_id))

        return resp
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout')
def logout():
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('user_id', '', expires=0)
    return resp

@app.route('/home', methods=['GET'])
def get_movies():
    user_id = request.cookies.get('user_id', None)

    cursor.execute('SELECT setup_complete FROM user WHERE user_id="{0}"'.format(user_id))
    for row in cursor:
        if not row[0]:
            return redirect('/new_user/services')

    services = []
    cursor.execute('SELECT service_id FROM userService WHERE user_id="{0}"'.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        services.append(str(row[0]))
    
    watchedMovies = []
    cursor.execute('SELECT movie_id FROM watchedMovies WHERE user_id="{0}"'.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        watchedMovies.append(row[0])
    
    userScore = {}
    cursor.execute('SELECT genre_id, user_score FROM userScore WHERE user_id="{0}"'.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        userScore[str(row[0])] = row[1]
    
    movies = default_movies_for_user(userScore, services, 10, watchedMovies)
    
    for x in movies:
        genre_names = []
        service_names = []
        for y in x['genre_ids']:
            cursor.execute('SELECT genre_name FROM genre WHERE genre_id="{0}"'.format(y))
            rows = cursor.fetchall()
            for row in rows:
                genre_names.append(row)
            x['genre_names'] = genre_names
        for y in x['source']:
            cursor.execute('SELECT service_name FROM service WHERE service_id="{0}"'.format(y))
            rows = cursor.fetchall()
            for row in rows:
                service_names.append(row)
            x['service_names'] = service_names

    return render_template('./home.html', movies=movies, base64 = base64)

@app.route('/search',methods=['POST'])
def submit():
    request_data = request.form
    movie_list = get_imdb_movie(request_data['title'])
    print(movie_list)
    return render_template('./info_page.html', movie_list=movie_list)

@app.route('/movie_info', methods=['POST'])
def movie_submit():
    request_data = request.form
    tmdb_id = tmdbid_from_imdbid(request_data['imdb_id'])
    sources = sources_from_tmdbid(tmdb_id)
    return render_template('./movie_info.html', movie_sources=sources)

@app.route('/new_user/services', methods = ['GET'])
def new_user_services():
    services=[]
    cursor.execute('SELECT * FROM service')
    for row in cursor:
        services.append(row)
    return render_template('./new_user_sources.html',streaming_services=services)

@app.route('/new_user/services/submit', methods = ['POST'])
def new_user_services_submit():
    user_id = request.cookies.get('user_id', None)
    request_data = request.form.getlist('service')
    for service_id in request_data:
        cursor.execute('INSERT INTO userService VALUES ({0}, {1})'.format(user_id, service_id))
    conn.commit()
    return redirect('/new_user/genres')

@app.route('/new_user/genres', methods=['GET'])
def new_user_genres():
    display_movies = initial_movie_display()
    return render_template('./new_user_genres.html', movietitles = display_movies)

@app.route('/new_user/genres/submit', methods=['POST'])
def new_user_genres_submit():
    user_id = request.cookies.get('user_id', None)

    request_data = request.form.getlist('movie')
    genrescores = clean_genres(request_data)
    genres = get_genres()
    userscore = {}
    for genre in genres:
       userscore[genre[0]] = 5
    new_userscores = update_userscores(userscore, genrescores)

    for (genre_id, score) in new_userscores.items():
        cursor.execute('INSERT INTO userScore VALUES ({0}, {1}, {2}) ON DUPLICATE KEY UPDATE user_score={2}'.format(user_id, genre_id, score))

    cursor.execute('UPDATE user SET setup_complete=1 WHERE user_id={0}'.format(user_id))
    conn.commit()

    return redirect('/home')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

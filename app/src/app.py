from secrets import SECRETS

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flaskext.mysql import MySQL
import os

app = Flask(__name__, template_folder="templates")
mysql = MySQL()

# Ignore that connection is not HTTPS (for local testing)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '130Barnes'
app.config['MYSQL_DATABASE_DB'] = 'userInfo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app.secret_key = SECRETS['flask_secret_key']
app.config['GOOGLE_OAUTH_CLIENT_ID'] = SECRETS['google_client_id']
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = SECRETS['google_client_secret']

google_bp = make_google_blueprint(scope=['email'], offline=True)
app.register_blueprint(google_bp, url_prefix='/login')

conn = mysql.connect()
cursor = conn.cursor()

def isEmailUnique(email):
    cursor = conn.cursor()
    if cursor.execute("SELECT user_email  FROM user WHERE user_email = '{0}'".format(email)):
        return False
    else:
        return True

@app.route('/')
def index():
    if google.authorized:
        resp = google.get('/oauth2/v1/userinfo')
        assert resp.ok, resp.text
        if isEmailUnique(resp.json()['email']) == True:
            cursor.execute("INSERT INTO user (user_email) VALUES ('{0}')" .format(resp.json()['email']))
            conn.commit()
        return render_template('home.html',email=resp.json()['email'])
    else:
        return render_template('index.html')



@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout')
def logout():
    try:
        del google_bp.token
    except:
        print('no Google OAuth token to delete')

    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

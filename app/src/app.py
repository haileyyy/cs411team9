from secrets import SECRETS

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import os

app = Flask(__name__, template_folder="templates")

# Ignore that connection is not HTTPS (for local testing)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app.secret_key = SECRETS['flask_secret_key']
app.config['GOOGLE_OAUTH_CLIENT_ID'] = SECRETS['google_client_id']
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = SECRETS['google_client_secret']

google_bp = make_google_blueprint(scope=['email'], offline=True)
app.register_blueprint(google_bp, url_prefix='/login')

@app.route('/')
def index():
    if google.authorized:
        resp = google.get('/oauth2/v1/userinfo')
        assert resp.ok, resp.text
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

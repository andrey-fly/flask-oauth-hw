from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from auth_decorator import login_required
import requests
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# oauth config
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/drive.readonly'},
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
)

@app.route('/')
@login_required
def main_page():
    email = dict(session).get('email', None)
    return f'<p>Hello, {email} !</p>'

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    print(redirect_uri)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    session['access_token'] = token['access_token']
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/drive')
def drive():
    answer = requests.get('https://www.googleapis.com/drive/v2/files?orderBy=title_natural', 
    headers={'Authorization': f"Bearer {session['access_token']}"})
    answer_json = answer.json()
    items_list = answer_json['items']
    titles_list = ''
    for item in items_list:
        titles_list += f"<p>{item['title']}</p>"
    return titles_list

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
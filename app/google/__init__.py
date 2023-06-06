from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
blueprint = make_google_blueprint(
    client_id='<client-id>',
    client_secret='<client-secret>',
    scope=['profile', 'email'],
    redirect_url='/google/login/authorized'
)
app.register_blueprint(blueprint, url_prefix='/login')

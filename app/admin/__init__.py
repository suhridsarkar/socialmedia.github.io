from flask import Flask, session, redirect, render_template
from app.main import main_bp
from app.auth import auth_bp
from app.chat import chat_bp
from app.comment import comment_bp
from app.friend import friend_bp
from app.post import post_bp
from app.setting import setting_bp
from app.models import db
import os

# DATABASE = os.path.join(os.path.dirname(__file__), "site.db")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
# root_db.init_app(app)
# with app.app_context():
#     root_db.create_all()
# cors = CORS(app)
# app.secret_key = "hhdhdhdhdh7788768"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialMedia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.secret_key = 'PUTUSUHRID'
UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POST_UPLOAD_FOLDER'] = UPLOAD_FOLDER + 'post/'
app.config['PROFILE_UPLOAD_FOLDER'] = UPLOAD_FOLDER + 'profile/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

with app.app_context():
    db.create_all()

@app.before_request
def check_auth():
    userId = session.get('uid')
    if not userId:
        redirect("/ddd")
    else:
        redirect("/auth/login")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Not Found")


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(post_bp)
app.register_blueprint(setting_bp)
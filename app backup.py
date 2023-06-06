from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey, create_engine, or_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import datetime
# from database import execute_query
# from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# from app import  db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialMedia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'PUTUSUHRID'
db = SQLAlchemy(app)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
# app.config['MAIL_PASSWORD'] = '*****'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)
# create a session
# Sessionmigrate = Migrate(app, db)
# create the engine and session
# engine = create_engine('sqlite:///socialMediaNew03.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# define the User and Friend models
# Base = declarative_base()
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Gender(Enum):
    M = 'M'
    F = 'F'
    C = 'C'

class RelationshipStatus(Enum):
    M = 'M'
    S = 'S'
    UM = 'UM'
    W = 'W'

class Action(Enum):
    Y = 'Y'
    N = 'N'
# Y = Active, N = InActive

class RequestStatus(Enum):
    N = 'N'
    A = 'A'
    R = 'R'
    B = 'B'
# 0= requested(N), 1 = friend request accepted(A), 2= regect(R), 3 = block(B)

class SeeYourPost(Enum):
    O = 'O'
    F = 'F'
    FE = 'FE'
    SF = 'SF'
    P = 'P'
# O= only me(O), 1 = friendS(F), 2= Friends Exception(FE), 3 = Publick(p)

class TypeOfPost(Enum):
    P = 'P'
    S = 'S'
    R = 'R'
# P= Post(P), S = Story(S), R= Reels(R)

class notificationStatus(Enum):
    S = 'S'
    U = 'U'

# S= Seen(S), 1 = UnSeen(U)

class notificationIsFor(Enum):
    L = 'L'
    C = 'C'

# L= Like(S), C = Comment(C)

class seeType(Enum):
    SE = 'SE'
    FE = 'FE'

# FE= Friends exception, SE = Friends exception


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    useId = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200),unique=False, nullable=True)
    nickName = db.Column(db.String(200), unique=False, nullable=True)
    image = db.Column(db.String(200), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.Integer, unique=True, nullable=True)
    dateOfBirth = db.Column(db.String, unique=False, nullable=True)
    gender = db.Column(db.Enum(Gender), unique=False, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=True)
    adminPassword = db.Column(db.String(120), unique=False, nullable=True)
    bio = db.Column(db.String(120), unique=False, nullable=True)
    relationshipStatus = db.Column(db.Enum(RelationshipStatus), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    saveLoginInfo = db.Column(db.Enum(Action), unique=False, nullable=True)
    twoFactorAuthentication = db.Column(db.Enum(Action), unique=False, nullable=True)
    # notification = db.Column(db.Enum(Action), unique=False, nullable=True)


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    text = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(120), unique=False, nullable=True)
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    # like = db.Column(db.Integer, nullable=True)
    # comment = db.Column(db.Integer, nullable=True)
    # share = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class loginfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class chatGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, nullable=True)
    receiverId = db.Column(db.Integer, nullable=True)
    groupId = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, nullable=True)
    receiverId = db.Column(db.Integer, nullable=True)
    groupId = db.Column(db.Integer, nullable=True)
    messages = db.Column(db.String(255), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class seeYourPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, unique=False, nullable=True)
    userId = db.Column(db.Integer, unique=False, nullable=True)
    friendId = db.Column(db.Integer,  unique=False,  nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    isFor = db.Column(db.Enum(TypeOfPost), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class selectFriend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=False, nullable=True)
    friendId = db.Column(db.Integer,  unique=False,  nullable=True)
    seeType = db.Column(db.Enum(seeType), unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, unique=False, nullable=True)
    senderId = db.Column(db.Integer, nullable=True)
    receiverId = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    status = db.Column(db.Enum(notificationStatus), unique=False, nullable=True)
    isFor = db.Column(db.Enum(notificationIsFor), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    text = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(120), unique=False, nullable=True)
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

# class friends(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.Integer, ForeignKey('user.id'))
#     friendId = db.Column(db.Integer, ForeignKey('user.id'))
#     date = db.Column(db.String(20))

    # user = db.relationship('user', foreign_keys=[userId], backref='friends')
    # friend = db.relationship('user', foreign_keys=[friendId] )

class friendrequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    friendId = db.Column(db.Integer, ForeignKey('user.id'))
    status = db.Column(db.Enum(RequestStatus), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class passwordHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    oldPassword = db.Column(db.String(120), unique=False, nullable=True)
    newPassword = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)

class postComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    postId = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(255), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class CommentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('user', backref=db.backref('comments', lazy=True))
    post = db.relationship('post', backref=db.backref('comments', lazy=True))

# class postSubComment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
#     commentId = db.Column(db.Integer, nullable=False)
#     comment = db.Column(db.String(255), nullable=False)
#     ip = db.Column(db.String(120), unique=False, nullable=True)
#     isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
#     logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user = db.relationship('user', backref=db.backref('comments', lazy=True))
#     post = db.relationship('post', backref=db.backref('comments', lazy=True))


class postLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    postId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

    def __repr__(self):
        return '<User %r>' % self.name
with app.app_context():
    db.create_all()


# post.__table__.drop()

# # session = db.session
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POST_UPLOAD_FOLDER'] = UPLOAD_FOLDER + 'post/'
app.config['PROFILE_UPLOAD_FOLDER'] = UPLOAD_FOLDER + 'profile/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# @app.route("/friends")
# def friendslist():
#         if session.get('uid'):
#             loguid = session.get('uid')



#             # subquery = db.session.query(friends.friendId).filter(friends.userid == loguid).subquery()
#             # result = db.session.query(user).outerjoin(friends, and_(user.id == friends.friendId, friends.userid == loguid)).filter(friends.friendId == None, user.id != loguid).all()
#             # subquery =  friends.query(friends.friendId)
#             # subquery = db.session.query(friends.friendId).filter(friends.userid == loguid).subquery()
#             # result = db.session.query(user).filter(user.id.notin_(subquery)).filter(user.id != loguid).all()
#             return render_template('friends.html',friends=result)
#         else:
#             return redirect('/welcome')


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)


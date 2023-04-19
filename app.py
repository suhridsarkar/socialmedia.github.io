from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey, create_engine, or_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import datetime
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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def greet():
    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        return "Good Morning"
    elif hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"
@app.route("/")
def home():
   userId = session.get('uid')
#    friends = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == uid, friendrequests.status == RequestStatus.A)

   if userId:
        # user_id = 2  # the user ID for whom you want to fetch the posts

        # posts = db.session.query(post, user).\
        #         join(user, user.id == post.userId).\
        #         filter(and_(
        #             or_(
        #                 post.seeYourPost == 'P',
        #                 post.id.in_(db.session.query(friendrequests.userId).filter_by(friendId=2, status='A'))
        #             ),
        #             or_(
        #                 post.id.in_(db.session.query(friendrequests.friendId).filter_by(userId=2, status='A'))
        #             )
        #         )).\
        #         filter(post.userId != 2)
        # user_id = 2  # the user ID for whom you want to fetch the posts
    # SQL
    # SELECT * FROM 'post' JOIN user ON user.id = post.userId WHERE ( post.seeYourPost = 'P' OR (post.id IN ( SELECT userID FROM 'friendrequests' WHERE friendId = 2 AND status = 'A')) OR post.id IN (SELECT friendId FROM 'friendrequests' WHERE userID = 2 AND status = 'A')) AND post.userId != 2 
        posts = db.session.query(post, user).select_from(post).join(user,user.id == post.userId).filter(
            and_(
                or_(
                    post.seeYourPost == 'P',
                    post.id.in_(db.session.query(friendrequests.userId).filter(and_(friendrequests.friendId == userId, friendrequests.status == 'A'))),
                    post.id.in_(db.session.query(friendrequests.friendId).filter(and_(friendrequests.userId == userId, friendrequests.status == 'A')))
                ),
                post.userId != userId
            )
        )
        results = posts.all()
        userdata = user.query.filter(user.id == userId).first()
        return render_template('home.html', greet = greet(), user = userdata, posts = results)
   else:
        return redirect('/welcome')
    #return render_template('home.html')

@app.route("/home")
def homepage():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()

        return render_template('home.html',  greet = greet(), user = userdata)
    else:
        return redirect('/welcome')

@app.route("/welcome")
def welcome ():
    return render_template('welcome.html')

@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    userId = session.get('uid')
    if userId:
        return render_template('register.html')
    else:
        return redirect('/welcome')

def generate_id():
    unique_id = str(uuid.uuid4().int)[:10]
    return unique_id

# @app.route("/testnew", methods=['POST','GET'])
# def testnew():
#     uid = generate_id()
#     return uid

@app.route("/userRegister", methods=['POST','GET'])
def userValidation():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            gender = request.form['gender']
            dob = request.form['dob']
            password = request.form['password']
            adminPassword = request.form['password']
            hashed_password = generate_password_hash(password, method='sha256')
            current_datetime = datetime.datetime.now()
            date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            client_ip_address = request.remote_addr
            unique_id = generate_id()
            userdata = user.query.filter(or_(user.phone == phone, user.email == email))
            if userdata is not None:
                new_user = user(useId= unique_id,name=name, email=email, phone = phone, gender = gender, dateOfBirth = dob,  password=hashed_password, adminPassword =  adminPassword, ip = client_ip_address, date = date, isActive=Action.Y )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                 return render_template('register.html')
        return render_template('register.html')

@app.route("/updataUser", methods=['POST','GET'])
def updataUser():
        userId = session.get('uid')
        userData = db.session.query(user).filter_by(id=userId).first()
        if request.method == 'POST':
            name = request.form['name']
            userData.nickName = request.form['nickName']
            # image = request.form['image']
            # email = request.form['email']
            # phone = request.form['phone']
            userData.dateOfBirth = request.form['dateOfBirth']
            userData.gender = request.form['gender']
            userData.bio = request.form['bio']
            current_datetime = datetime.datetime.now()
            userData.date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            userData.ip = request.remote_addr
            # userdata = user.query.filter(or_(user.phone == phone, user.email == email))
            # if userdata is not None:
            # new_user = user(name=name, email=email, phone = phone, gender = gender, dateOfBirth = dateOfBirth,  password=hashed_password, adminPassword =  adminPassword, ip = client_ip_address, date = date, isActive=Action.Y )
            if 'image' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['image']
            if file.filename == '':
                flash('No image selected for uploading')
                # return redirect(request.url)
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename))
                    print('upload_image filename: ' + filename)

                    # cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
                    # conn.commit()

                    flash('Image successfully uploaded and displayed below')
                    # return render_template('index.html', filename=filename)
                    userData.image = filename
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')
            
            # new_user = user(name=name, dateOfBirth = dateOfBirth, ip = client_ip_address, date = date, isActive=Action.Y )
            # db.session.add(new_user)
            db.session.commit()
            # return redirect(url_for('login'))
            # else:
            #      return render_template('register.html')
        return redirect(url_for('editProfile'))



#    name = request.form.get("name")
#    email = request.form.get("email")
#    password = base64.b64encode(request.form.get("password").encode("utf-8"))
#    adminPassword = request.form.get("password")
#    userValidation= user.query.filter_by(email=email).first()
#    if userValidation:
#         return redirect('/register')
#    else:
#         current_datetime = datetime.datetime.now()
#         date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#         client_ip_address = request.remote_addr
#         user_test = user(name=name, email=email, password=password, adminPassword =  adminPassword, ip = client_ip_address, date = date)
#         db.session.add(user_test)
#         db.session.commit()
#         # msg = Message('Hello', sender = 'suhridsarkar, recipients = ['someone1@gmail.com'])
#         # msg.body = "This is the email body"
#         # mail.send(msg)
#         return redirect('/login')


@app.route("/userlogin", methods=['POST'])
def loginValidation():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        userdet = user.query.filter_by(email=email).first()
        if userdet and check_password_hash(userdet.password, password):
            logid = generate_id()
            uid = userdet.id
            session['uid'] = uid
            session['email'] = email
            current_datetime = datetime.datetime.now()
            date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            client_ip_address = request.remote_addr
            
            logdata = loginfo(userId= uid, ip = client_ip_address, date = date, isActive=Action.Y )
            # logdata = loginfo(useId= uid, logid = logid, latitud=latitud, longitude = longitude, ip = client_ip_address, date = date, isActive=Action.Y )
            db.session.add(logdata)
            db.session.commit()
            session['logid'] = logdata.id
            # session['test'] = 'ewwe'
            # print(logdata.id)
            return redirect(url_for('homepage'))
    return render_template('login.html')



@app.route("/forgotPassword")
def forgotPassword():
    return render_template('forgotPassword.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route("/createPost")
def createPost():
    
    if session.get('uid'):
        userId = session.get('uid')
        subquery1 = db.session.query(friendrequests.friendId).filter(friendrequests.userId == userId, friendrequests.status == 'A').subquery()
        subquery2 = db.session.query(friendrequests.userId).filter(friendrequests.friendId == userId, friendrequests.status == 'A').subquery()
        friendsList = db.session.query(user.id, user.name, user.image).filter((user.id.in_(subquery1)) | (user.id.in_(subquery2))).all()
        return render_template('createPost.html', friendsList = friendsList)
    else:
        return redirect('/welcome')


@app.route("/savePost", methods=['POST','GET'])
def savePost():
    logid = session.get('logid')
    text = request.form.get("description")
    seeYourPost = request.form.get("seeYourPost")
    client_ip_address = request.remote_addr
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    filename = ''
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No image selected for uploading')
        # return redirect(request.url)
    else:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['POST_UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' + filename)

            # cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
            # conn.commit()

            flash('Image successfully uploaded and displayed below')
            # return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            # return redirect(request.url)
    # postData = post(text=text, userId=session.get('uid'),image=filename, seeYourPost=seeYourPost,location = location, latitud = latitud, longitude = longitude, ip = client_ip_address, date = date, isActive = Action.Y)
    postData = post(text=text, userId=session.get('uid'),image=filename, seeYourPost=seeYourPost, ip = client_ip_address, date = date, isActive = Action.Y)
    # postData = post(description=description, ip = client_ip_address, date = date)
    db.session.add(postData)
    db.session.commit()
    selectFriendData = db.session.query(selectFriend).filter_by(userId = session.get('uid'), seeType = seeYourPost)
    # for data in selectFriendData:
    #     insertData = seeYourPost(postId = postData.id, userId=session.get('uid'),friendId=data.friendId, isFor=TypeOfPost.P, date = date, isActive = Action.Y, logid = logid)
    #     db.session.add(insertData)
    #     db.session.commit()
    # selectFriendData = db.session.query(selectFriend).filter_by(userId = session.get('uid'), seeType = seeYourPost).delete()

    return redirect('/createPost')


@app.route("/seePost", methods=['POST'])
def seePost():
    id = request.form.get("id")
    type = request.form.get("type")
    action = request.form.get("action")
    userId = session.get('uid')
    if action == '1':
        newData = selectFriend(userId=userId, friendId=id, seeType =  type,isActive = Action.Y)
        db.session.add(newData)
        db.session.commit()
    else:
        selectFriend.query.filter_by(userId = userId, friendId=id, seeType = type).delete()
        db.session.commit()
    return '1'

@app.route("/lodeFriendList", methods=['POST'])
def lodeFriendList():
    # action = request.form.get("action")
    userId = session.get('uid')
    subquery1 = db.session.query(friendrequests.friendId).filter(friendrequests.userId == userId, friendrequests.status == 'A').subquery()
    subquery2 = db.session.query(friendrequests.userId).filter(friendrequests.friendId == userId, friendrequests.status == 'A').subquery()
    friendsList = db.session.query(user.id, user.name, user.image).filter((user.id.in_(subquery1)) | (user.id.in_(subquery2))).all()

    selectFriend.query.filter_by(userId = userId).delete()
    db.session.commit()
    return render_template('lodeFriendList.html',friendsList=friendsList)

@app.route("/profile")
def profile():
    userId = session.get('uid')
    # userdata = user.query.filter(id==userId)
    if userId:
        userdata = db.session.query(user).filter(user.id == userId).first()
        return render_template('profile.html',user= userdata, userdata=userdata)
    else:
        return redirect('/welcome')
    
@app.route("/editProfile")
def editProfile():
    userId = session.get('uid')
    # userdata = user.query.filter(id==userId)
    userdata = db.session.query(user).filter(user.id == userId).first()
    return render_template('editProfile.html',user = userdata, userdata=userdata)

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

@app.route("/friends")
def friendslist():
        userId = session.get('uid')
        # result = db.session.query(user)
        if userId:
            # subquery1 = db.session.query(friends.friendId).filter(friends.userid == uid).subquery()
            subquery2 = db.session.query(friendrequests.friendId).filter(friendrequests.userId == userId).subquery()
            # result = db.session.query(user).filter(user.id.notin_(subquery1), user.id.notin_(subquery2),).filter(user.id != uid).all()
            userlist = db.session.query(user).filter(user.id.notin_(subquery2),user.id != userId)
            friendRequestsList = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == userId, friendrequests.status == RequestStatus.N)
            totalRequested = friendRequestsList.count()
            # print(totalRequested)
            userdata = user.query.filter(user.id == userId).first()
            return render_template('friends.html',greet = greet(), user = userdata, friend=userlist, totalRequested = totalRequested, friendRequestsList= friendRequestsList)
        else:
            return redirect('/welcome')

# @app.route("/sentfriendrequests", methods=['POST'])
# def sentfriendrequests():
    # fid = request.form.get("id")
    # uid = session.get('uid')
    # current_datetime = datetime.datetime.now()
    # date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # client_ip_address = request.remote_addr
    # # newRequest = user(userid=uid, friendId=fid, status =  0, ip = client_ip_address, date = date, is_active = 'Y')
    # newRequest = friendrequests(userid=uid, friendId=fid, status =  0, date = date)
    # db.session.add(newRequest)
    # db.session.commit()
    # return redirect('/createPost')

@app.route("/actionrequests", methods=['POST'])
def confirmfriendrequests():
    id = request.form.get("id")
    action = request.form.get("action")
    uid = session.get('uid')
    logid = session.get('logid')
    if action == '2':
        friend_request = db.session.query(friendrequests).filter_by(id=id).first()
        friend_request.status = RequestStatus.R
        db.session.commit()
    elif action == '1':
        friend_request = db.session.query(friendrequests).filter_by(id=id).first()
        friend_request.status = RequestStatus.A
        db.session.commit()
    elif action == '0':
        # # sent friend requests
        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        client_ip_address = request.remote_addr
        # newRequest = user(userid=uid, friendId=id, status =  0, ip = client_ip_address, date = date, is_active = 'Y')
        newRequest = friendrequests(userId=uid, friendId=id, status =  RequestStatus.N,ip=client_ip_address, date = date, isActive = Action.Y, logid = logid)
        db.session.add(newRequest)
        db.session.commit()
    return "1"

@app.route("/chats")
def chats():
        userId = session.get('uid')
        # result = db.session.query(user)
        if userId:
            friendslist = db.session.query(user).filter(
                # and_(
                    or_(
                        user.id.in_(db.session.query(friendrequests.userId).filter(and_(friendrequests.friendId == userId, friendrequests.status == 'A'))),
                        user.id.in_(db.session.query(friendrequests.friendId).filter(and_(friendrequests.userId == userId, friendrequests.status == 'A')))
                    ),
                #     user.logstatus != userId
                # )
                
            )
            userdata = user.query.filter(user.id == userId).first()
            return render_template('chats.html',greet = greet(), user = userdata, friendslist = friendslist)
        else:
            return redirect('/welcome')
@app.route("/chat/<friendId>")
def chat(friendId):
        userId = session.get('uid')
        # result = db.session.query(user)
        if userId:
            # friendslist = db.session.query(user).filter(
            #     # and_(
            #         or_(
            #             user.id.in_(db.session.query(friendrequests.userId).filter(and_(friendrequests.friendId == userId, friendrequests.status == 'A'))),
            #             user.id.in_(db.session.query(friendrequests.friendId).filter(and_(friendrequests.userId == userId, friendrequests.status == 'A')))
            #         ),
            #     #     user.logstatus != userId
            #     # )
            # )
            userdata = user.query.filter(user.id == userId).first()
            return render_template('chat.html',greet = greet(), user = userdata, friendslist = friendslist)
        else:
            return redirect('/welcome')



if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)


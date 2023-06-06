from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey, create_engine, or_
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_basefrom flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey, create_engine, or_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from datetime import datetime
from flask_ckeditor import CKEditorField
db = SQLAlchemy()



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
class fileType(Enum):
    I = 'Image'
    V = 'Video'

# I= Image, V = Video


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
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    saveLoginInfo = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    twoFactorAuthentication = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    # notification = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)

class adminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200),unique=False, nullable=True)
    image = db.Column(db.String(200), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.Integer, unique=True, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)

class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    text = db.Column(db.String(50), nullable=True)
    file = db.Column(db.String(120), unique=False, nullable=True)
    fileType = db.Column(db.Enum(fileType), default=fileType.I, unique=False, nullable=True)
    # CO
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    like = db.Column(db.Integer, nullable=True, default= 0)
    comment = db.Column(db.Integer, nullable=True, default= 0)
    share = db.Column(db.Integer, nullable=True, default= 0)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('postUser', lazy=True))

class loginfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('loginfouser', lazy=True))

class chatGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    groupId = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    senderUser = db.relationship('user',foreign_keys=[senderId], backref=db.backref('sender_user', lazy=True))
    receverUser = db.relationship('user', foreign_keys=[receiverId], backref=db.backref('recever_user', lazy=True))

class chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    groupId = db.Column(db.Integer, nullable=True)
    messages = db.Column(db.String(255), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    senderUser = db.relationship('user', foreign_keys=[senderId], backref=db.backref('senderUser', lazy=True))
    receverUser = db.relationship('user', foreign_keys=[receiverId], backref=db.backref('receverUser', lazy=True))

class seeYourPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    friendId = db.Column(db.Integer,  unique=False,  nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    isFor = db.Column(db.Enum(TypeOfPost), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('seeYourPostUser', lazy=True))
    post = db.relationship('post', foreign_keys=[postId], backref=db.backref('seeYourPostData', lazy=True))


class selectFriend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friendId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seeType = db.Column(db.Enum(seeType), unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    selectFriendUser = db.relationship('user', foreign_keys=[userId], backref=db.backref('selectFriendUser', lazy=True))
    selectFriendFriend = db.relationship('user', foreign_keys=[friendId], backref=db.backref('selectFriendFriend', lazy=True))

class notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, unique=False, nullable=True)
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    receiverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    status = db.Column(db.Enum(notificationStatus), unique=False, nullable=True)
    isFor = db.Column(db.Enum(notificationIsFor), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    notificationSender = db.relationship('user', foreign_keys=[senderId], backref=db.backref('notificationSender', lazy=True))

class story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    text = db.Column(db.String(50), nullable=True)
    file = db.Column(db.String(120), unique=False, nullable=True)
    fileType = db.Column(db.Enum(fileType), default=fileType.I, unique=False, nullable=True)
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    like = db.Column(db.Integer, nullable=True, default= 0)
    comment = db.Column(db.Integer, nullable=True, default= 0)
    share = db.Column(db.Integer, nullable=True, default= 0)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('storyUserNew', lazy=True))
class storyNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    text = db.Column(db.String(50), nullable=True)
    file = db.Column(db.String(120), unique=False, nullable=True)
    fileType = db.Column(db.Enum(fileType), default=fileType.I, unique=False, nullable=True)
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    like = db.Column(db.Integer, nullable=True, default= 0)
    comment = db.Column(db.Integer, nullable=True, default= 0)
    share = db.Column(db.Integer, nullable=True, default= 0)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('storyUser', lazy=True))

class reels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    text = db.Column(db.String(50), nullable=True)
    file = db.Column(db.String(120), unique=False, nullable=True)
    fileType = db.Column(db.Enum(fileType), default=fileType.I, unique=False, nullable=True)
    seeYourPost = db.Column(db.Enum(SeeYourPost), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    latitud = db.Column(db.String(120), unique=False, nullable=True)
    longitude = db.Column(db.String(120), unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    like = db.Column(db.Integer, nullable=True, default= 0)
    comment = db.Column(db.Integer, nullable=True, default= 0)
    share = db.Column(db.Integer, nullable=True, default= 0)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    user = db.relationship('user', foreign_keys=[userId], backref=db.backref('reelsUser', lazy=True))


# class friends(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.Integer, ForeignKey('user.id'))
#     friendId = db.Column(db.Integer, ForeignKey('user.id'))
#     date = db.Column(db.String(20))
    # user = db.relationship('user', foreign_keys=[userId], backref='friends')
    # friend = db.relationship('user', foreign_keys=[friendId] )

class reelsLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    postId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class friendrequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey('user.id'))
    friendId = db.Column(db.Integer, ForeignKey('user.id'))
    status = db.Column(db.Enum(RequestStatus), unique=False, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
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
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)

# class postComment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, nullable=True)
#     postId = db.Column(db.Integer, nullable=True)
#     comment = db.Column(db.String(255), unique=False, nullable=True)
#     ip = db.Column(db.String(120), unique=False, nullable=True)
#     date = db.Column(db.String, unique=False, nullable=True)
#     isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
#     logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class commentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('user', backref=db.backref('comments', lazy=True))
    post = db.relationship('post', backref=db.backref('comments', lazy=True))

class postSubComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    commentId = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('user', backref=db.backref('postSubComment', lazy=True))
    post = db.relationship('post', backref=db.backref('postSubComment', lazy=True))


class postLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    postId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))
class storyLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=True)
    storyId = db.Column(db.Integer, nullable=True)
    ip = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class about(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))

class privacyPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    date = db.Column(db.String, unique=False, nullable=True)
    isActive = db.Column(db.Enum(Action), default=Action.N, unique=False, nullable=True)
    logid = db.Column(db.Integer, ForeignKey('loginfo.id'))


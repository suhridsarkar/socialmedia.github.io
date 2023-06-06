from flask import current_app, Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests,notification, db, selectFriend, Action, fileType, notificationStatus, notificationIsFor
from app.commen import greet, generate_id, allowed_file
from datetime import datetime
from werkzeug.utils import secure_filename
import os

post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/createPost")
def createPost():
    
    if session.get('uid'):
        userId = session.get('uid')
        subquery1 = db.session.query(friendrequests.friendId).filter(friendrequests.userId == userId, friendrequests.status == 'A').subquery()
        subquery2 = db.session.query(friendrequests.userId).filter(friendrequests.friendId == userId, friendrequests.status == 'A').subquery()
        friendsList = db.session.query(user.id, user.name, user.image).filter((user.id.in_(subquery1)) | (user.id.in_(subquery2))).all()
        userdata = user.query.filter(user.id == userId).first()

        return render_template('createPost.html',title ="Post", friendsList = friendsList, user = userdata)
    else:
        return redirect('/welcome')


@post_bp.route("/savePost", methods=['POST','GET'])
def savePost():
    logid = session.get('logid')
    text = request.form.get("description")
    seeYourPost = request.form.get("seeYourPost")
    client_ip_address = request.remote_addr
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    filename = ''
    file_type = fileType.I
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
            file.save(os.path.join(current_app.config['POST_UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' + filename)
            file_ext = os.path.splitext(filename)[1]
            print(file_ext)
            if file_ext == '.mov' or file_ext == '.mp4': 
                file_type = fileType.V
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            # return redirect(request.url)
    # postData = post(text=text, userId=session.get('uid'),image=filename, seeYourPost=seeYourPost,location = location, latitud = latitud, longitude = longitude, ip = client_ip_address, date = date, isActive = Action.Y)
    postData = post(text=text, userId=session.get('uid'),fileType = file_type, file=filename, seeYourPost=seeYourPost, ip = client_ip_address, date = date, isActive = Action.Y)
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


@post_bp.route("/seePost", methods=['POST'])
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

# # # # # # # # # # # # # # # # # #
# Like Insert Data
# # # # # # # # # # # # # # # # # #
@post_bp.route("/postLikeInsert", methods=['POST'])
def postLikeInsert():
    userId = session.get('uid')
    postId = request.form["id"]
    logid = session.get('logid')
    client_ip_address = request.remote_addr
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    queryData = postLike.query.filter(postLike.userId == userId, postLike.postId == postId).first()
    postData = post.query.filter(post.id == postId).first()
    if queryData:
        if queryData.isActive == Action.N:
            # notificationAdd = notification(senderId=userId,receiverId=postData.userId, postId=postId, status= notificationStatus.U,isFor = notificationIsFor.L, date = date, isActive = Action.Y, logid = logid)
            # # db.session.add(postLikeAdd)
            # db.session.add(notificationAdd)

            queryData.isActive = Action.Y
            if postData.like:
                postData.like = int(postData.like)+1
            else:
                postData.like = 1
        else:
            # # # # # # # # # # # # # # # # # #
            # Like Update Data
            # # # # # # # # # # # # # # # # # #
            queryData.isActive = Action.N
            if postData.like:
                postData.like = int(postData.like)-1
            else:
                postData.like = 1
    else:
        postLikeAdd = postLike(userId=userId, postId=postId, ip=client_ip_address, date = date, isActive = Action.Y, logid = logid)
        db.session.add(postLikeAdd)
        notificationAdd = notification(senderId=userId,receiverId=postData.userId, postId=postId, status= notificationStatus.U,isFor = notificationIsFor.L, date = date, isActive = Action.Y, logid = logid)
        db.session.add(notificationAdd)
        # db.session.add(postLikeAdd)
    db.session.commit()
    return '1'
    
    # return render_template('lodeComment.html',chats = chats, friend = friend)

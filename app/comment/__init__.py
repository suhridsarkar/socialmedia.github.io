from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, commentData, postSubComment, Action, notificationStatus, notificationIsFor, notification
from app.commen import greet, generate_id
from datetime import datetime

comment_bp = Blueprint("comment_bp", __name__)

       
@comment_bp.route("/comment/<postId>")
def commentView(postId):
       
        userId = session.get('uid')
        if userId:
            userdata = user.query.filter(user.id == userId).first()
            comments = commentData.query.filter(postId == postId).all()
            return render_template('comment.html', title = "Comment" ,greet = greet(), postId = postId, comments = comments, userdata = userdata)
        else:
            return redirect('/welcome')
        

# def getData(table , field='', value=''):
#     if field != '' and value != '':
#         return table.query.filter(table.field == value)
#     else:
#         return table.query()

# @comment_bp.route("/lodeComment")
# def lodeComment():
#     userId = session.get('uid')
#     postId = request.form["postId"]
#     data = postComment.query.filter(userId == userId, postId == postId).all()
#     print(data)
#     return '1'

@comment_bp.route("/insertComment", methods=['POST'])
def insertComment():

    userId = session.get('uid')
    # userId = 5
    # comment = request.form.get("comment")
    isSubComment = request.form.get("isSubComment")
    comment = request.form["comment"]
    postId = request.form["postId"]
    logid = session.get('logid')
    client_ip_address = request.remote_addr
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    postData = post.query.filter(post.id == postId).first()

    if isSubComment == '0':
        commentAdd = commentData(userId=userId, comment=comment, postId=postId, ip=client_ip_address, isActive = Action.Y, logid = logid)
        if postData.comment:
            postData.comment = int(postData.comment)+1
        else:
             postData.comment = 1

    else: 
        commentAdd = postSubComment(userId=userId,commentId = isSubComment, comment=comment, postId=postId, ip=client_ip_address, isActive = Action.Y, logid = logid)
        if postData.comment:
            postData.comment = int(postData.comment)+1
        else:
             postData.comment = 1
    db.session.add(commentAdd)
    notificationAdd = notification(senderId=userId,receiverId=postData.userId, postId=postId, status= notificationStatus.U,isFor = notificationIsFor.C, date = date, isActive = Action.Y, logid = logid)
    db.session.add(notificationAdd)
    db.session.commit()
    comments = commentData.query.filter(postId == postId).all()
    return render_template('lodeComment.html', comments = comments) 
    # return render_template('lodeComment.html',chats = chats, friend = friend)


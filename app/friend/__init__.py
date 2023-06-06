from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, selectFriend, RequestStatus, Action
from app.commen import greet, generate_id
from datetime import datetime

friend_bp = Blueprint("friend_bp", __name__)


@friend_bp.route("/lodeFriendList", methods=['POST'])
def lodeFriendList():
    # action = request.form.get("action")
    userId = session.get('uid')
    subquery1 = db.session.query(friendrequests.friendId).filter(friendrequests.userId == userId, friendrequests.status == 'A').subquery()
    subquery2 = db.session.query(friendrequests.userId).filter(friendrequests.friendId == userId, friendrequests.status == 'A').subquery()
    friendsList = db.session.query(user.id, user.name, user.image).filter((user.id.in_(subquery1)) | (user.id.in_(subquery2))).all()

    selectFriend.query.filter_by(userId = userId).delete()
    db.session.commit()
    return render_template('lodeFriendList.html',friendsList=friendsList)

@friend_bp.route("/friends")
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
            return render_template('friends.html', title = "Friends",greet = greet(), user = userdata, friend=userlist, totalRequested = totalRequested, friendRequestsList= friendRequestsList)
        else:
            return redirect('/welcome')


@friend_bp.route("/actionrequests", methods=['POST'])
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
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        client_ip_address = request.remote_addr
        # newRequest = user(userid=uid, friendId=id, status =  0, ip = client_ip_address, date = date, is_active = 'Y')
        newRequest = friendrequests(userId=uid, friendId=id, status =  RequestStatus.N,ip=client_ip_address, date = date, isActive = Action.Y, logid = logid)
        db.session.add(newRequest)
        db.session.commit()
    return "1"


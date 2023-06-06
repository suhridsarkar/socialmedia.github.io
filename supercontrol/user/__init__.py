from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, Action, storyNew, storyLike
from app.commen import greet, generate_id
from jinja2 import Environment

user_bp = Blueprint("user_bp", __name__)



@user_bp.route("/usermanagement")
def userManagement():
    # print(session.get('uid'))
    userId = session.get('adminUserId')
#    friends = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == uid, friendrequests.status == RequestStatus.A)

    if userId is not None:
            userdata = db.session.query(user).filter(user.isActive == Action.Y).order_by(user.id.desc()).all()
            thead = ['Name','Email', 'Phone', 'Date Of Birth','Gender' ,'Date', 'Is Active'];
            tbody = ['name','email', 'phone', 'dateOfBirth','gender', 'date', 'isActive'];
            return render_template('userTable.html', title = 'Dashboard',users = userdata, thead = thead, tbody = tbody)
    else:
            return redirect('/login')
    #return render_template('home.html')

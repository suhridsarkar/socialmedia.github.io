from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, Action, storyNew, storyLike
from app.commen import greet, generate_id
from jinja2 import Environment

dashboard_bp = Blueprint("dashboard_bp", __name__)



@dashboard_bp.route("/dashboard")
def dashboard():
    # print(session.get('uid'))
    userId = session.get('adminUserId')
#    friends = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == uid, friendrequests.status == RequestStatus.A)

    if userId is not None:
            return render_template('dashboard.html', title = 'Dashboard')
    else:
            return redirect('/login')
    #return render_template('home.html')

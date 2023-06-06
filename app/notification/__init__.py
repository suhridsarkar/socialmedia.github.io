from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, Action, notification
from app.commen import greet, generate_id


notification_bp = Blueprint("notification_bp", __name__)


@notification_bp.route("/notification")
def notificationView():
    
    if session.get('uid'):
        userId = session.get('uid')
        notificationData = db.session.query(notification).filter(notification.receiverId == userId).order_by(notification.id.desc()).all()
        userdata = user.query.filter(user.id == userId).first()

        return render_template('notification.html',title ="Notification", greet = greet(), user = userdata, notification = notificationData)
    else:
        return redirect('/welcome')

from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, loginfo, Action
from app.commen import greet, generate_id

setting_bp = Blueprint("setting_bp", __name__)



# # # # # # # # # # # # # # # # # #
# Setting View
# # # # # # # # # # # # # # # # # #
@setting_bp.route("/setting")
def setting():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()
        return render_template('setting.html', title = "Setting" ,greet = greet(), user = userdata)
    else:
        return redirect('/welcome')
    

# # # # # # # # # # # # # # # # # #
# Update Notification Setting
# # # # # # # # # # # # # # # # # #
@setting_bp.route("/updateNotification", methods=['post'])
def updateNotificationSetting():
    userId = session.get('uid')
    # userdata = user.query.filter(user.id == userId).first()
    # if userdata.notification == Action.Y:
    #     userdata.notification = Action.N
    # else:
    #     userdata.notification = Action.Y
    # db.session.commit()
    return '1'

    
# # # # # # # # # # # # # # # # # #
# Security Page View
# # # # # # # # # # # # # # # # # #
    
@setting_bp.route("/security")
def security():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()
        loginfodata = loginfo.query.filter(loginfo.userId == userId)
        return render_template('security.html', title = "Security" ,greet = greet(), user = userdata, loginfodata = loginfodata)
    else:
        return redirect('/welcome')
    
# # # # # # # # # # # # # # # # # #
# Update Two factor authentication
# # # # # # # # # # # # # # # # # #

@setting_bp.route("/updateTwoFactorAuthentication", methods=['post'])
def updateTwoFactorAuthentication():
    userId = session.get('uid')
    userdata = user.query.filter(user.id == userId).first()
    if userdata.twoFactorAuthentication == Action.Y:
        userdata.twoFactorAuthentication = Action.N
    else:
        userdata.twoFactorAuthentication = Action.Y
    db.session.commit()
    return '1'
    
# # # # # # # # # # # # # # # # # #
# Logout From Login Info Page
# # # # # # # # # # # # # # # # # #

@setting_bp.route("/logoutfromloginfo", methods=['post'])
def logoutfromloginfo():
    id = request.form["id"]
    loginfodata = loginfo.query.filter(loginfo.id == id).first()
    if loginfodata.isActive == Action.Y:
        loginfodata.isActive = Action.N
    else:
        loginfodata.isActive = Action.Y
    db.session.commit()
    return '1'
   
# # # # # # # # # # # # # # # # # #
# About Page View
# # # # # # # # # # # # # # # # # #
    
@setting_bp.route("/about")
def about():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()
        loginfodata = loginfo.query.filter(loginfo.userId == userId)
        return render_template('about.html', title = "Security" ,greet = greet(), user = userdata, loginfodata = loginfodata)
    else:
        return redirect('/welcome')
    
   
# # # # # # # # # # # # # # # # # #
# Terms Page View
# # # # # # # # # # # # # # # # # #
    
@setting_bp.route("/terms")
def terms():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()
        loginfodata = loginfo.query.filter(loginfo.userId == userId)
        return render_template('terms.html', title = "Security" ,greet = greet(), user = userdata, loginfodata = loginfodata)
    else:
        return redirect('/welcome')
    
   
# # # # # # # # # # # # # # # # # #
# Privacy Policy Page View
# # # # # # # # # # # # # # # # # #
    
@setting_bp.route("/privacyPolicy")
def privacyPolicy():
    userId = session.get('uid')
    if userId:
        userdata = user.query.filter(user.id == userId).first()
        loginfodata = loginfo.query.filter(loginfo.userId == userId)
        return render_template('privacyPolicy.html', title = "Security" ,greet = greet(), user = userdata, loginfodata = loginfodata)
    else:
        return redirect('/welcome')
    
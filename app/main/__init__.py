from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db, Action, storyNew, storyLike
from app.commen import greet, generate_id
from jinja2 import Environment

main_bp = Blueprint("main_bp", __name__)


def my_split(value):
    return value.split()

env = Environment()
env.filters['my_split'] = my_split
@main_bp.route("/")
def home():
    # print(session.get('uid'))
    userId = session.get('uid')
#    friends = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == uid, friendrequests.status == RequestStatus.A)

    if userId is not None:
            # SQL
            # SELECT * FROM 'post' JOIN user ON user.id = post.userId WHERE ( post.seeYourPost = 'P' OR (post.id IN ( SELECT userID FROM 'friendrequests' WHERE friendId = 2 AND status = 'A')) OR post.id IN (SELECT friendId FROM 'friendrequests' WHERE userID = 2 AND status = 'A')) AND post.userId != 2 
            posts = db.session.query(post, user, postLike.userId.label('like_user_id')).select_from(post).join(user,user.id == post.userId).outerjoin(postLike, and_(post.id == postLike.postId, postLike.userId == userId, postLike.isActive == Action.Y)).filter(
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

            story = db.session.query(storyNew, user, storyLike.userId.label('like_user_id')).select_from(post).join(user,user.id == post.userId).outerjoin(storyLike, and_(post.id == storyLike.storyId, storyLike.userId == userId, storyLike.isActive == Action.Y)).filter(
                and_(
                    or_(
                        post.seeYourPost == 'P',
                        post.id.in_(db.session.query(friendrequests.userId).filter(and_(friendrequests.friendId == userId, friendrequests.status == 'A'))),
                        post.id.in_(db.session.query(friendrequests.friendId).filter(and_(friendrequests.userId == userId, friendrequests.status == 'A')))
                    ),
                    post.userId != userId
                )
            )
            userdata = user.query.filter(user.id == userId).first()
            return render_template('home.html', title = 'Home', greet = greet(), user = userdata, posts = results, storys = story.all())
    else:
            return redirect('/welcome')
    #return render_template('home.html')

@main_bp.route("/home")
def homepage():
   userId = session.get('uid')
#    friends = db.session.query(user.name, friendrequests.id ).join(friendrequests, user.id == friendrequests.userId).filter(friendrequests.friendId == uid, friendrequests.status == RequestStatus.A)

   if userId:

    # # # SQL # # #
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
        return render_template('home.html', title = 'Home', greet = greet(), user = userdata, posts = results)
  
   else:
        return redirect('/welcome')
    #return render_template('home.html')

@main_bp.route("/welcome")
def welcome ():
    return render_template('welcome.html', title = 'Welcome')

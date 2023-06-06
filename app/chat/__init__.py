from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, chat,friendrequests, db
from app.commen import greet, generate_id
from datetime import datetime

chat_bp = Blueprint("chat_bp", __name__)


@chat_bp.route("/chats")
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
            # SQL
            # SELECT * FROM 'user' where 	(senderId = 5 OR receiverId = 2) group by groupId
            chats = db.session.query(user, chat).join(chat, or_(user.id == chat.senderId, user.id == chat.receiverId)).filter(
                   
                        or_(
                        chat.senderId == userId, chat.receiverId == userId, 
                        )
            ).group_by(chat.groupId).all()
            # db.session.query(User, Chat)
            # .join(Chat, (user1.id == Chat.sender_id) | (user2.id == Chat.receiver_id))
            # .filter((Chat.sender_id == 5) | (Chat.receiver_id == 2))
            # .group_by(Chat.group_id)
            # .all()
            userdata = user.query.filter(user.id == userId).first()
            return render_template('chats.html', title = "Chats",greet = greet(), user = userdata, friendslist = friendslist, chats = chats)
        else:
            return redirect('/welcome')
        
@chat_bp.route("/chat/<friendId>")
def chatlist(friendId):
        # num_rows_deleted = db.session.query(chat).delete()
        # db.session.commit()
        userId = session.get('uid')
        # result = db.session.query(user)
        if userId:
            # SQL
            # SELECT * FROM 'chat' where 	(senderId = 5 AND receiverId = 2) OR (senderId = 2 AND receiverId = 5)
            chats = db.session.query(chat).filter(
                    or_(
                        and_(
                        chat.senderId == userId, chat.receiverId == friendId, 
                        ),
                        and_(
                        chat.receiverId == userId, chat.senderId == friendId, 
                        )
                    ),
               
            ).all()
            # chats = chat.query.filter(
            #     or_(
            #         chat.sender_id == 5, chat.receiver_id == 5,
            #         chat.sender_id == 2, chat.receiver_id == 2,
            #     ),
            #     chat.sender_id != chat.receiver_id,
            # ).all()
            print(chats)
            userdata = user.query.filter(user.id == userId).first()
            friend = user.query.filter(user.id == friendId).first()
            return render_template('chat.html', title = "Chat",greet = greet(), user = userdata, friend = friend, chats = chats)
        else:
            return redirect('/welcome')
        
@chat_bp.route("/sendMessages", methods=['POST'])
def sendMessages():


    userId = session.get('uid')
    # userId = 5
    messages = request.form.get("messages")
    friendId = request.form.get("friend")
    # friendId = 2
    logid = session.get('logid')
    client_ip_address = request.remote_addr
    current_datetime = datetime.now()
    date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    chats = db.session.query(chat).filter(
        or_(
            and_(
            chat.senderId == userId, chat.receiverId == friendId, 
            ),
            and_(
            chat.receiverId == userId, chat.senderId == friendId, 
            )
        ),
    
    ).first()
    if chats:
        chatAdd = chat(senderId=userId, receiverId=friendId, groupId=chats.groupId, messages =  messages, ip=client_ip_address, date = date, isActive = Action.Y, logid = logid)
        db.session.add(chatAdd)
        db.session.commit()
    else:
        
        chatAdd = chat(senderId=userId, receiverId=friendId, groupId = generate_id(), messages =  messages, ip=client_ip_address, date = date, isActive = Action.Y, logid = logid)
        db.session.add(chatAdd)
        db.session.commit()
    friend = user.query.filter(user.id == friendId).first()
    chats = db.session.query(chat).filter(
        or_(
            and_(
            chat.senderId == userId, chat.receiverId == friendId, 
            ),
            and_(
            chat.receiverId == userId, chat.senderId == friendId, 
            )
        ),
    
    ).all()

    return render_template('lodeChat.html',chats = chats, friend = friend)

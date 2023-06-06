from flask import current_app, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import loginfo, user, postLike,friendrequests, db, Action
from app.commen import greet, generate_id, allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# for file uplode
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login")
def login():
    return render_template('login.html', title = 'Login')


@auth_bp.route("/register")
def register():
    
    return render_template('register.html', title = 'Register')


# @auth_bp.route("/testnew", methods=['POST','GET'])
# def testnew():
#     uid = generate_id()
#     return uid

@auth_bp.route("/userRegister", methods=['POST','GET'])
def userValidation():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            gender = request.form['gender']
            dob = request.form['dob']
            password = request.form['password']
            adminPassword = request.form['password']
            hashed_password = generate_password_hash(password, method='sha256')
            current_datetime = datetime.now()
            date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            client_ip_address = request.remote_addr
            unique_id = generate_id()
            userdata = user.query.filter(or_(user.phone == phone, user.email == email))
            if userdata is not None:
                new_user = user(useId= unique_id,name=name, email=email, phone = phone, gender = gender, dateOfBirth = dob,  password=hashed_password, adminPassword =  adminPassword, ip = client_ip_address, date = date, isActive=Action.Y )
                db.session.add(new_user)
                db.session.commit()
                flash('You have successfully registered!, Please Login.', 'success')
                return redirect('/login')
            else:
                 flash('Registration failed. Please try again.', 'danger')
                 return render_template('register.html', title = 'Register')
        flash('Registration failed. Please try again.', 'danger')
        return render_template('register.html', title = 'Register')

@auth_bp.route("/updataUser", methods=['POST','GET'])
def updataUser():
        userId = session.get('uid')
        userData = db.session.query(user).filter_by(id=userId).first()
        if request.method == 'POST':
            name = request.form['name']
            userData.nickName = request.form['nickName']
            # image = request.form['image']
            # email = request.form['email']
            # phone = request.form['phone']
            userData.dateOfBirth = request.form['dateOfBirth']
            userData.gender = request.form['gender']
            userData.bio = request.form['bio']
            current_datetime = datetime.now()
            userData.date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            userData.ip = request.remote_addr
            # userdata = user.query.filter(or_(user.phone == phone, user.email == email))
            # if userdata is not None:
            # new_user = user(name=name, email=email, phone = phone, gender = gender, dateOfBirth = dateOfBirth,  password=hashed_password, adminPassword =  adminPassword, ip = client_ip_address, date = date, isActive=Action.Y )
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
                    if not os.path.exists(current_app.config['PROFILE_UPLOAD_FOLDER']):
                        os.makedirs(current_app.config['PROFILE_UPLOAD_FOLDER'])
                    file.save(os.path.join(current_app.config['PROFILE_UPLOAD_FOLDER'], filename))
                    print('upload_image filename: ' + filename)

                    # cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
                    # conn.commit()

                    flash('Image successfully uploaded and displayed below', )
                    # return render_template('index.html', filename=filename)
                    userData.image = filename
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')
            
            # new_user = user(name=name, dateOfBirth = dateOfBirth, ip = client_ip_address, date = date, isActive=Action.Y )
            # db.session.add(new_user)
            db.session.commit()
            # return redirect(url_for('login'))
            # else:
            #      return render_template('register.html')
        flash('Profile updated successfully!', 'success')
    # flash('Error updating profile. Please try again.', 'error')

        return redirect('/editProfile')





@auth_bp.route("/userlogin", methods=['POST'])
def loginValidation():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        userdet = db.session.query(user).filter_by(email=email).first()
        print(email)
        print(userdet)
        if userdet and check_password_hash(userdet.password, password):
            logid = generate_id()
            uid = userdet.id
            session['uid'] = uid
            session['email'] = email
            current_datetime = datetime.now()
            date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            client_ip_address = request.remote_addr
            
            logdata = loginfo(userId= uid, ip = client_ip_address, date = date, isActive=Action.Y )
            # logdata = loginfo(useId= uid, logid = logid, latitud=latitud, longitude = longitude, ip = client_ip_address, date = date, isActive=Action.Y )
            db.session.add(logdata)
            db.session.commit()
            session['logid'] = logdata.id
            # session['test'] = 'ewwe'
            # print(logdata.id)
            flash('Login successful!', 'success')

            return redirect('/')
        flash('Incorrect username or password. Please try again.', 'danger')
    flash('Incorrect username or password. Please try again.', 'danger')
    return render_template('login.html', title = 'Login')



@auth_bp.route("/forgotPassword")
def forgotPassword():
    return render_template('forgotPassword.html', title = 'Forgot Password')
#WIP
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'success')

    return redirect('/')


@auth_bp.route("/profile")
def profile():
    userId = session.get('uid')
    # userdata = user.query.filter(id==userId)
    if userId:
        userdata = db.session.query(user).filter(user.id == userId).first()
        return render_template('profile.html', title = "Profile",user= userdata, userdata=userdata)
    else:
        return redirect('/welcome')
    
@auth_bp.route("/editProfile")
def editProfile():
    userId = session.get('uid')
    # userdata = user.query.filter(id==userId)
    userdata = db.session.query(user).filter(user.id == userId).first()
    return render_template('editProfile.html',user = userdata, userdata=userdata, title = "Edit Profile")

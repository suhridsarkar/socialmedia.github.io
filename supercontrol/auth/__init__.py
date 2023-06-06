from flask import current_app, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import adminUser, Action, db
from app.commen import greet, generate_id, allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .forms import RegistrationForm, LoginForm

# for file uplode
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint("auth_bp", __name__, template_folder="templates")

@auth_bp.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form=form)


@auth_bp.route("/adminvalidation", methods=['POST'])
def loginValidation():
    if request.method == 'POST':

        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            # hashed_password = generate_password_hash(password, method='sha256')
            # current_datetime = datetime.now()
            # date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # adminUserAdd = adminUser(username=username, name='SuperControl', password=password, date = date, isActive = Action.Y)
            # db.session.add(adminUserAdd)
            # db.session.commit()

            verify_user = db.session.query(adminUser).filter_by(username=username, password=password).first()
            if verify_user:
                    session["adminUserName"] = username
                    session["adminUserId"] = verify_user.id
                    return redirect(url_for("dashboard_bp.dashboard"))
            else:
                flash('Incorrect username or password. Please try again. 2', 'danger')
                return redirect(url_for("auth_bp.login"))
        else:
            flash('Please Enter Valid Username And Password. 3', 'danger')
            return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'success')

    return redirect('/')

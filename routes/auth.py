""" Authorization routes for the app """
# ------ THIRD PARTY IMPORTS -----
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

# ----- PROJECT IMPORTS -----
from extensions import db
from models import User, UserCreationSchema

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    form_data = request.form
    error_message = 'Sorry, we were unable to log you in. The username and password \
        you provided did not match our records. Please check your login details and try again.\
         If you continue to experience issues, please contact our support team for assistance.'
    username = form_data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(error_message)
        return redirect(url_for('auth.login'))

    if check_password_hash(user.password, form_data.get('password')):
        login_user(user)
        return redirect(url_for('views.profile'))
    else:
        flash(error_message)
        return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return render_template('auth/login.html')


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    form_data = request.form

    try:
        add_user_schema = UserCreationSchema()                  # password hashed in creation
        new_user = add_user_schema.load(form_data)

        db.session.add(new_user)
        db.session.commit()
    except ValidationError as err:
        error_messages = err.messages
        db.session.rollback()
        return render_template('auth/signup.html', error_messages=error_messages)
    flash('User added!')
    return redirect(url_for('auth.login'))


@auth.route("/check_username")
def check_username():
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


@auth.route("/check_email")
def check_email():
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})

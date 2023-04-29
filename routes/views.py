""" General routes for the app """

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import UserSchema

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def index():
    return render_template('index.html')


@views.route('/profile')
@login_required
def profile():
    user_schema = UserSchema()
    user = user_schema.dump(current_user)
    return render_template('profile.html', user=user)



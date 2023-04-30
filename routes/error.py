""" General routes for the app """

from flask import Blueprint, flash, redirect, render_template, url_for

error = Blueprint('error', __name__)


@error.app_errorhandler(401)
def unauthorized_error(e):
    """ Redirect on 401 Error """
    flash('You must be logged in to view this content')
    return redirect(url_for('auth.login'))


@error.app_errorhandler(403)
def forbidden_error(e):
    """ Redirect on 403 Error """
    return redirect(url_for('error.forbidden'))


@error.route('/forbidden')
def forbidden():
    """ Custom 403 page """
    return render_template('error/forbidden.html')


@error.app_errorhandler(404)
def not_found_error(e):
    """ Redirect on 404 Error """
    return redirect(url_for('error.not_found'))


@error.route('/not_found')
def not_found():
    """ Custom 404 page """
    return render_template('error/not_found.html')


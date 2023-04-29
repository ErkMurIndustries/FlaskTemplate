""" Run to create app """

# ----- IMPORTS ----
from flask import Flask
from dotenv import load_dotenv, set_key
from extensions import db, env_path, login_manager, ma
from models import *


def create_app(app_name):
    """ Creates and configures app """
    app = Flask(app_name)

    load_config(app)
    register_blueprints(app)
    register_addons(app)

    with app.app_context():
        """ Creates SQL tables from models """
        db.create_all()

    return app


def load_config(app):
    """ Load config settings """
    load_dotenv(env_path)
    app.config.from_prefixed_env()

    if not app.config.get('SECRET_KEY'):
        add_secret_key(app)

    if not app.config.get('ENCRYPTION_KEY'):
        add_encryption_key(app)

    return


def add_secret_key(app):
    """ Generates secret key and adds to config """
    import secrets
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    set_key(env_path, 'FLASK_SECRET_KEY', secret_key)
    return


def add_encryption_key(app):
    """ Generates an encryption key """
    from cryptography.fernet import Fernet
    encryption_key = Fernet.generate_key()
    app.config['ENCRYPTION_KEY'] = encryption_key.decode()
    set_key(env_path, 'FLASK_ENCRYPTION_KEY', encryption_key.decode())
    return


def register_blueprints(app):
    """ Load blueprints into app """
    from routes import auth, error, views
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(error, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return


def register_addons(app):
    """ Register addons to app """
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return


if __name__ == "__main__":
    app = create_app('app_name')
    app.run(debug=True)

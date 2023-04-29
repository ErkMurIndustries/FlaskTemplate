""" Instantiate Flask add ons """

# ----- IMPORTS -----
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

# Database ORM
db = SQLAlchemy()

# Schema serialization
ma = Marshmallow()

# Login management
login_manager = LoginManager()

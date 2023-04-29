# ----- IMPORTS -----
from extensions import db, ma
from flask_login import UserMixin
from marshmallow import fields, validates, ValidationError, post_load
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    """ User definition """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password',)


class UserCreationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, username, **kwargs):
        # Check if the username is unique
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValidationError('Username already exists')

    @validates('email')
    def validate_email(self, email, **kwargs):
        # Check if the email is unique
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValidationError('Email already exists')

    @validates('password')
    def validate_password(self, password, **kwargs):
        # Check if password meets the criteria
        errors = []
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        if not any(char.isupper() for char in password):
            errors.append('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            errors.append('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            errors.append('Password must contain at least one number')
        if errors:
            raise ValidationError(errors)

    @post_load
    def load_user(self, data):
        user = User(
            username=data["username"],
            email=data['email'],
            password=generate_password_hash(data['password'], method='scrypt'),
        )
        return user

from datetime import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    imageUrl = db.Column(db.String(255), unique=True)
    body = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('UserModel', back_populates='posts')

    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "title": self.title
        }


class UserModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, nullable=False)

    posts = db.relationship("PostModel", back_populates="author")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def json(self):
        return {
            "name": self.first_name + ' ' + self.last_name,
            "id": self.id,
            "username": self.username
                }

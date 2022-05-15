import jwt
import environ
import os

env = environ.Env(DEBUG=(bool, False))
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
environ.Env.read_env(os.path.join(basedir, '.env'))
secret = os.environ['JWT_SECRET_KEY']


def create_jwt(user):
	return jwt.encode(
		{
			'userId': user.id,
			'username': user.username,
		},
		secret, algorithm="HS256")


def decode_jwt(token):
	return jwt.decode(token, secret, algorithms=["HS256"])


def is_user_authenticated(userId, token_userId):
	return userId == token_userId

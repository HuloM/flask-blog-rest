from flask import request, jsonify, make_response
from datetime import datetime as dt

from models import UserModel as User
from models import db
from util.error_handler import respond_error
from util.user_jwt import create_jwt


def user_signup():
	if request.method == 'PUT':
		email = request.form['email']

		userExists = User.query.filter_by(email=email).first()
		if userExists:
			return respond_error('This email is already registered with us, please login', 422)

		password = request.form['password']
		confirm_password = request.form['confirmPassword']
		if password != confirm_password:
			return respond_error('passwords must match', 422)

		first_name = request.form['first_name']
		last_name = request.form['last_name']
		username = request.form['username']

		user = User(
			email=email,
			username=username,
			# password hashing is done through the password.setter method in the user model
			password=password,
			first_name=first_name,
			last_name=last_name,
			createdAt=dt.now()
		)

		db.session.add(user)
		db.session.commit()
		return make_response(jsonify(
			{
				'message': 'user has been registered',
				'user': user.json()
			}), 200)


def user_login():
	if request.method == 'POST':
		email = request.form['email']
		userExists = User.query.filter_by(email=email).first()
		if userExists:
			password = request.form['password']
			if userExists.check_password(password):
				token = create_jwt(userExists)
				return make_response(jsonify(
					{
						'message': 'user has logged in',
						'token': token
					}), 200)
			else:
				return respond_error('incorrect password', 422)
		else:
			return respond_error('This email does not exist, please signup', 422)

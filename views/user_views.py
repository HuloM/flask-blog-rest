from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt

from models import UserModel as User
from models import db


def user_signup():
	if request.method == 'PUT':
		email = request.form['email']
		userExists = User.query.filter_by(email=email).first()
		if userExists:
			return make_response(jsonify(
				{
					'message': 'This email is already registered with us, please login',
				}), 422)
		password = request.form['password']
		confirm_password = request.form['confirmPassword']
		if password != confirm_password:
			return make_response(jsonify(
				{
					'message': 'passwords must match',
				}), 422)
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		username = request.form['username']
		user = User(
			email=email,
			username=username,
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
				return make_response(jsonify(
					{
						'message': 'user has logged in',
						'user': userExists.json()
					}), 200)
			else:
				return make_response(jsonify(
					{
						'message': 'incorrect password',
					}), 422)
		else:
			return make_response(jsonify(
				{
					'message': 'This email does not exist, please signup',
				}), 422)

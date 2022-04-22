from flask import request, jsonify, make_response
from datetime import datetime as dt

from models import PostModel as Post
from models import db
from util.error_handler import respond_401
from util.user_jwt import decode_jwt, is_user_authenticated


def RUD_post(index):
	requested_post = Post.query.get(index)
	if request.method == 'GET':
		return response_post('Post retrieved Successfully', requested_post)
	token = request.headers['Authorization']
	if token:
		decoded = decode_jwt(token)
		if is_user_authenticated(requested_post.author_id, decoded['userId']):
			if request.method == 'PUT':
				return update_post(requested_post)
			elif request.method == 'DELETE':
				return delete_post(requested_post)
		else:
			return respond_401('User is not author of post')
	return respond_401('Not Authorized')


def CR_posts():
	if request.method == 'POST':
		token = request.headers['Authorization']
		if token:
			decoded = decode_jwt(token)
			return create_post(decoded['userId'])
		else:
			return respond_401('Not Authorized')
	else:
		return retrieve_all_posts()


def retrieve_all_posts():
	return make_response(jsonify({
		'message': 'Posts retrieved successfully',
		'posts': [post.json() for post in db.session.query(Post).all()]
	}), 200)


def response_post(message, requested_post):
	return make_response(jsonify({
		'message': message,
		'post': requested_post.json()
	}), 200)


def delete_post(requested_post):
	db.session.delete(requested_post)
	db.session.commit()
	return response_post('Post deleted Successfully', requested_post)


def update_post(requested_post):
	title = request.form['title']
	body = request.form['body']
	imageUrl = request.form['image'] or requested_post.imageUrl
	requested_post.title = title
	requested_post.body = body
	requested_post.updatedAt = dt.now()
	if requested_post.imageUrl != imageUrl:
		# TODO delete old image
		requested_post.imageUrl = imageUrl
	db.session.commit()
	return response_post('Post updated Successfully', requested_post)


def create_post(userid):
	title = request.form['title']
	body = request.form['body']
	imageUrl = request.form['image'] + '-' + str(dt.now().timestamp())
	post = Post(
		title=title,
		imageUrl=imageUrl,
		body=body,
		author_id=userid,
		createdAt=dt.now(),
		updatedAt=dt.now()
	)
	db.session.add(post)
	db.session.commit()
	return response_post('Post created Successfully', post)

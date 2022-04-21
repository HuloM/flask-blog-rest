from flask import request, jsonify, make_response
from datetime import datetime as dt

from models import PostModel as Post
from models import db


def RUD_post(index):
	requested_post = Post.query.get(index)
	if request.method == 'PUT':
		return update_post(requested_post)
	elif request.method == 'DELETE':
		return delete_post(requested_post)
	return make_response(jsonify({
		'message': 'Post retrieved Successfully',
		'post': requested_post.json()
	}), 200)


def CR_posts():
	if request.method == 'POST':
		return create_post()
	else:
		return make_response(jsonify({
			'message': 'Posts retrieved successfully',
			'posts': [post.json() for post in db.session.query(Post).all()]
		}), 200)


def delete_post(requested_post):
	db.session.delete(requested_post)
	db.session.commit()
	return make_response(jsonify({
		'message': 'Post deleted Successfully',
		'post': requested_post.json()
	}), 200)


def update_post(requested_post):
	title = request.form['title']
	body = request.form['body']
	imageUrl = request.form['image']
	requested_post.title = title
	requested_post.body = body
	requested_post.updatedAt = dt.now()
	if requested_post.imageUrl != imageUrl:
		# TODO delete old image
		requested_post.imageUrl = imageUrl
	db.session.commit()
	return make_response(jsonify({
		'message': 'Post updated Successfully',
		'post': requested_post.json()
	}), 200)


def create_post():
	title = request.form['title']
	body = request.form['body']
	imageUrl = request.form['image'] + '-' + str(dt.now().timestamp())
	post = Post(
		title=title,
		imageUrl=imageUrl,
		body=body,
		author_id=None,
		createdAt=dt.now(),
		updatedAt=dt.now()
	)
	db.session.add(post)
	db.session.commit()
	return make_response(jsonify({
		'message': 'Post created Successfully',
		'post': post.json()
	}), 200)

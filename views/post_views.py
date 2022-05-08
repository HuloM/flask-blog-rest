import os

from flask import request, jsonify, make_response
from datetime import datetime as dt

from werkzeug.utils import secure_filename

from models import PostModel as Post, CommentModel as Comment
from models import db
from util.error_handler import respond_error
from util.user_jwt import decode_jwt, is_user_authenticated

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
file_upload = os.path.join(basedir, 'uploads/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def RUD_post(index):
	requested_post = Post.query.get(index)
	if requested_post is None:
		return respond_error('That post does not exist', 422)
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
			return respond_error('User is not author of post', 401)
	return respond_error('Not Authorized', 401)


def C_comments(index):
	requested_post = Post.query.get(index)
	token = request.headers['Authorization']
	if token and request.method == 'POST':
		decoded = decode_jwt(token)
		return create_comment_on_post(index, decoded['userId'])


def CR_posts():
	if request.method == 'POST':
		token = request.headers['Authorization']
		if token:
			decoded = decode_jwt(token)
			return create_post(decoded['userId'])
		else:
			return respond_error('Not Authorized', 401)
	else:
		return retrieve_all_posts()


def retrieve_all_posts():
	print('Retrieving all posts')
	return make_response(jsonify({
		'message': 'Posts retrieved successfully',
		'posts': [post.json() for post in db.session.query(Post).all()]
	}), 200)


def delete_post(requested_post):
	delete_image(requested_post.imageUrl)
	db.session.delete(requested_post)
	db.session.commit()
	return response_post('Post deleted Successfully', requested_post)


def update_post(requested_post):
	title = request.form['title'] or requested_post.title
	body = request.form['body'] or requested_post.body
	requested_post.title = title
	requested_post.body = body
	requested_post.updatedAt = dt.now()

	if 'image' in request.files:
		image = request.files['image']
		if image:
			if allowed_file(image.filename):
				delete_image(requested_post.imageUrl)
				filename = upload_image(image)
				requested_post.imageUrl = filename
			else:
				return respond_error('incorrect file type submitted (accepted: PNG, JPG, JPEG)', 422)
	db.session.commit()
	return response_post('Post updated Successfully', requested_post)


def create_post(userid):
	title = request.form['title']
	body = request.form['body']

	if 'image' not in request.files or title is None or body is None:
		return respond_error('issue validating inputs', 422)
	image = request.files['image']
	if image.filename == '':
		return respond_error('No image uploaded', 422)
	if image and allowed_file(image.filename):
		filename = upload_image(image)
	else:
		return respond_error('incorrect file type submitted (accepted: PNG, JPG, JPEG)', 422)
	post = Post(
		title=title,
		imageUrl=filename or None,
		body=body,
		author_id=userid,
		createdAt=dt.now(),
		updatedAt=dt.now()
	)
	db.session.add(post)
	db.session.commit()
	return response_post('Post created Successfully', post)


def upload_image(image):
	filename = str(dt.now().timestamp()) + '-' + secure_filename(image.filename)
	image.save(os.path.join(file_upload, filename))
	return filename


def delete_image(filename):
	os.remove(os.path.join(file_upload, filename))


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def response_post(message, requested_post):
	return make_response(jsonify({
		'message': message,
		'post': requested_post.json()
	}), 200)


def create_comment_on_post(postId, userId):
	user_comment = request.form['comment']
	comment = Comment(
		comment=user_comment,
		author_id=userId,
		post_id=postId,
		createdAt=dt.now()
	)
	db.session.add(comment)
	db.session.commit()
	return make_response(jsonify({
		'message': 'Comment created Successfully',
		'comment': comment.json()
	}), 200)

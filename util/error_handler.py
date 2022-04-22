from flask import make_response, jsonify


def respond_401(message):
	return make_response(jsonify({
		'message': message
	}), 401)


def respond_422(message):
	return make_response(jsonify(
		{
			'message': message,
		}), 422)

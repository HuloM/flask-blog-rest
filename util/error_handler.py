from flask import make_response, jsonify

def respond_error(message, status):
	return make_response(jsonify(
		{
			'message': message,
		}), status)

from flask import Flask, make_response, jsonify
from models import db, flask_bcrypt
import environ
import os
from views.user_views import user_signup, user_login
from views.post_views import CR_posts, RUD_post

env = environ.Env(DEBUG=(bool, False))
basedir = os.path.abspath(os.path.dirname(__file__))
environ.Env.read_env(os.path.join(basedir, '.env'))

app = Flask(__name__)

# config options
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = env('SECRET_KEY')
app.config['PORT'] = 8080
app.config['DEBUG'] = True

db.init_app(app)
flask_bcrypt.init_app(app)

app.app_context().push()

db.create_all()


@app.route('/signup', methods=['PUT'])
def signup():
	return user_signup()


@app.route('/login', methods=['POST'])
def login():
	return user_login()


@app.route('/post/<int:index>', methods=['GET', 'PUT', 'DELETE'])
def post(index):
	return RUD_post(index)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
	return CR_posts()


if __name__ == '__main__':
	app.run()

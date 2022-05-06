from flask import Flask, request
from models import db, flask_bcrypt
import environ
import os
from views.user_views import user_signup, user_login
from views.post_views import CR_posts, RUD_post, C_comments

env = environ.Env(DEBUG=(bool, False))
basedir = os.path.abspath(os.path.dirname(__file__))
environ.Env.read_env(os.path.join(basedir, '.env'))

app = Flask(__name__)

# config options
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = env('SECRET_KEY')
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads/images')

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


@app.route('/post/comments/<int:index>', methods=['POST'])
def comment(index):
	return C_comments(index)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
	return CR_posts()


if __name__ == '__main__':
	app.run(port=8080)

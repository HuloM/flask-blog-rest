from flask import Flask, send_file
from flask_cors import CORS

from models import db, flask_bcrypt
import environ
import os
from views.user_views import user_signup, user_login
from views.post_views import C_posts, RUD_post, C_comments, retrieve_all_posts
from flask_migrate import Migrate

env = environ.Env(DEBUG=(bool, False))
# basedir holds the path to the root of the project directory
basedir = os.path.abspath(os.path.dirname(__file__))
# reads variables from the .env file
environ.Env.read_env(os.path.join(basedir, '.env'))

application = Flask(__name__, static_url_path='',
					static_folder='uploads')
CORS(application, resources=r'/*')
# config options
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
application.config['DEBUG'] = True
application.config['ENV'] = 'development'
application.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads\\images')

db.init_app(application)
flask_bcrypt.init_app(application)

application.app_context().push()
migrate = Migrate(application, db)
db.create_all()


@application.route('/static/<path:path>')
def send_report(path):
	img_path = os.path.join(application.config['UPLOAD_FOLDER'], str(path))
	return send_file(img_path)


@application.route('/signup', methods=['PUT'])
def signup():
	return user_signup()


@application.route('/login', methods=['POST'])
def login():
	return user_login()


@application.route('/post/<int:index>/', methods=['GET', 'PUT', 'DELETE'])
def post(index):
	return RUD_post(index)


@application.route('/post/comments/<int:index>', methods=['POST'])
def comment(index):
	return C_comments(index)


@application.route('/posts', methods=['POST'])
def CreatePost():
	return C_posts()


@application.route('/posts/<int:page>/', defaults={'page': 1})
def posts(page):
	return retrieve_all_posts(page)


if __name__ == '__main__':
	application.run(port=8080)

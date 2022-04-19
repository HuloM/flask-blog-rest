from flask import Flask
from models import db, flask_bcrypt
import environ
import os

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


if __name__ == '__main__':
	app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path=os.path.join('/bionetbay-dev', 'static'))

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from sqlalchemy import create_engine

if "SQLALCHEMY_DATABASE_URI" in os.environ.keys():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    # app.config['MAIL_SERVER']=os.environ["MAIL_SERVER"]
    # app.config['MAIL_PORT']=465
    # app.config['MAIL_USE_SSL']=True
    # app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
    # app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]

    app.config['BCRYPT_LOG_ROUNDS'] = 12

else:
    app.config.from_object('config')
db = SQLAlchemy(app)

app.vars = {}

from flask_mail import Mail
mail = Mail(app)

from bionetbay import views, models

from flask_login import LoginManager
from bionetbay import models

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"
login_manager.login_message_category = "alert alert-warning"

@login_manager.user_loader
def load_user(userid):
    return models.Users.query.filter(models.Users.id==userid).first()

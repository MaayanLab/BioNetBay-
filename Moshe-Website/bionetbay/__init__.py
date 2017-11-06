from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from sqlalchemy import create_engine

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

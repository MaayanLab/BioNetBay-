from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from sqlalchemy import create_engine

app.config.from_object('config')
db = SQLAlchemy(app)

app.vars = {}

from bionetbay import views, models

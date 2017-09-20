from flask import Flask

app = Flask(__name__)

app.vars = {}

from bionetbay import views

from flask import Flask
from flask_sqlalchemy import SQLAlchemy #import for SQL Alchemy
from flask_migrate import Migrate       #import for db migrations
from config import Config
from flask_login import LoginManager    #for login manager 1

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

app.run(debug=True)
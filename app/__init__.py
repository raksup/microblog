from flask import Flask
from flask_sqlalchemy import SQLAlchemy #import for SQL Alchemy
from flask_migrate import Migrate       #import for db migrations
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.config.from_object(Config)

from app import routes, models
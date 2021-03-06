from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from flask.globals import request
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy #import for SQL Alchemy
from flask_migrate import Migrate       #import for db migrations
from config import Config
from flask_login import LoginManager    #for login manager 1
import logging
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

app.config.from_object(Config)          #imports all the Config
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(mailhost= (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),\
                                    fromaddr= 'no-reply@'+app.config['MAIL_SERVER'],\
                                    toaddrs= app.config['ADMINS'],\
                                    subject='Microblog Internal Error',\
                                    credentials= auth, secure= secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors
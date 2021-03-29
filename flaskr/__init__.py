import os
from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from .celery_utils import init_celery
from .config import Config
from flask_sqlalchemy import SQLAlchemy


# create and configure the app
app = Flask(__name__, instance_relative_config=True)

#config.py
app.config.from_object(Config)
print(Config.SQLALCHEMY_DATABASE_URI)

#celery
celery = Celery(__name__, backend='rpc://', broker='amqp://localhost')
init_celery(celery, app)

#Setup DB/Migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Register Blueprints
from . import index
app.register_blueprint(index.bp)
app.add_url_rule('/', endpoint='index')

from . import all
app.register_blueprint(all.bp)

from flaskr import models
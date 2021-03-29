import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u lose sucker, haha!'
    CELERY_BACKEND_URL = os.environ.get('CELERY_BACKEND')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or 'sqlite:////') + os.path.join(basedir, 'flaskr.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
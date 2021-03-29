import os
from celery import Celery
from flask import Flask
from .celery_utils import init_celery


celery = Celery(__name__, backend='rpc://', broker='amqp://localhost')


def create_app(test_config=None, app_name=__name__, **kwargs):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config.update(
        CELERY_BACKEND_URL=os.environ.get('CELERY_BACKEND'),
        CELERY_BROKER_URL=os.environ.get('CELERY_BROKER')
    )

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:////' + os.path.join(basedir, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    celery.conf.update(app.config)

    from . import db
    db.init_app(app)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import all
    app.register_blueprint(all.bp)

    return app

from flask import (
    Blueprint, render_template
)
from flaskr.models import Alert

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    alerts = Alert.query.order_by(Alert.id.desc()).limit(10).all()

    return render_template('index.html', alerts=alerts)

from flask import (
    Blueprint, render_template
)

from flaskr.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    alerts = get_alerts()

    return render_template('index.html', alerts=alerts)


def get_alerts():
    db = get_db()

    alerts = db.execute(
        'SELECT sku, product, atc_url, product_url, created'
        ' FROM alerts'
        ' ORDER BY created DESC'
        ' LIMIT 10;'
    )

    return alerts

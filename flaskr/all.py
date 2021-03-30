from flask import Blueprint, request
import os
from .tasks import fetch_stock_info
from .models import Alert
from flaskr import app, db


bp = Blueprint("all", __name__)


# I dont even think I need this here anymore since celery is doing some work
@bp.route('/post', methods=['POST'])
def post():
    content = request.get_json()
    error = None

    if not request.is_json:
        error = "Invalid JSON"
    if not content:
        error = "Error converting JSON"

    if error:
        abort(Response(error))


    alert = Alert(sku=content['sku'], product=content['product'], atc_url=content['atc_url'], product_url=content['product_url'])
    db.session.add(alert)
    db.commit()

    return 'Nice one'


# Returns just the data portion of the table so this can be used as a hot refresh
@bp.route('/refresh')
def refresh():
    alerts = Alert.query.order_by(Alert.id.desc()).limit(10).all()
    result = ''

    # r = fetch_stock.delay()
    # print(r.result)

    for alert in alerts:
        result = result + \
            f'<tr><td>{ alert.sku }</td><td>{ alert.product }</td><td><a target=_blank href="{ alert.atc_url }" class="link-success">LINK</a></td><td><a target=_blank href="{ alert.product_url }" class="link-success">LINK</a></td><td>{ alert.created }</td></tr>'


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Alert':Alert}
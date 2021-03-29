from flask import Blueprint, request
import os
from .index import get_alerts
from .tasks import fetch_stock_info
from .db import get_db
bp = Blueprint("all", __name__)


# I dont even think I need this here anymore since celery is doing some work
@bp.route('/post', methods=['POST'])
def post():
    content = request.get_json()
    db = get_db()
    error = None

    if not request.is_json:
        error = "Invalid JSON"
    if not content:
        error = "Error converting JSON"

    if error:
        abort(Response(error))

    db.execute(
        'INSERT INTO alerts (sku, product, atc_url, product_url)'
        ' VALUES (?, ?, ?, ?);',
        (content['sku'], content['product'],
         content['atc_url'], content['product_url'])
    )
    db.commit()

    return 'Nice one'


# Returns just the data portion of the table so this can be used as a hot refresh
@bp.route('/refresh')
def refresh():
    alerts = get_alerts()
    result = ''

    # r = fetch_stock.delay()
    # print(r.result)

    for alert in alerts:
        result = result + \
            f'<tr><td>{ alert["SKU"] }</td><td>{ alert["product"] }</td><td><a target=_blank href="{ alert["atc_url"] }" class="link-success">LINK</a></td><td><a target=_blank href="{ alert["product_url"] }" class="link-success">LINK</a></td><td>{ alert["created"] }</td></tr>'

    return result

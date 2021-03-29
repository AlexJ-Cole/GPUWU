from flaskr import celery, db
from .models import Alert
from celery import chain
from datetime import datetime
from .GPUWU_server import fetchData, fetchDataMulti


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, update_stock.s(), expires=10)


@celery.task(name='update_stock')
def update_stock():
    g = chain(fetch_stock_info.s() | store_stock_info.s())
    g()


@celery.task(name='fetch_stock_info')
def fetch_stock_info():
    res = fetchDataMulti(
        'https://www.bestbuy.com/site/computer-cards-components/computer-pc-processors/abcat0507010.c?id=abcat0507010')
    return res


@celery.task(name='store_stock_info')
def store_stock_info(stock):
    for item in stock:
        alert = Alert(sku=item['sku'], product=item['product'], atc_url=item['atc_url'], product_url=item['product_url'])
        db.session.add(alert)
        db.session.commit()

    print("Successfully stored stock info")

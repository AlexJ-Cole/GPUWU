from flaskr import celery
from celery import chain
from .GPUWU_server import fetchData, fetchDataMulti
from .db import get_db


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
        'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?cp=3&id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090')
    return res


@celery.task(name='store_stock_info')
def store_stock_info(stock):
    db = get_db()

    for item in stock:
        db.execute(
            'INSERT INTO alerts (sku, product, atc_url, product_url)'
            ' VALUES (?, ?, ?, ?);',
            (item['sku'], item['product'],
             item['atc_url'], item['product_url'])
        )
        db.commit()

    print("Successfully stored stock info")

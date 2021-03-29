from flaskr import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, index=True)
    product = db.Column(db.String(256))
    atc_url = db.Column(db.String(64))
    product_url = db.Column(db.String(128))
    created = Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<Alert: { id }>'
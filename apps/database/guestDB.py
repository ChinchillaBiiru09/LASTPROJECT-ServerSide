from .. import db
from sqlalchemy.sql import func


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    alias = db.Column(db.String(60), nullable=True)
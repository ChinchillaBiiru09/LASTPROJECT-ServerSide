from .. import db
from sqlalchemy.sql import func


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    alias = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Guest {}>'.format(self.name)
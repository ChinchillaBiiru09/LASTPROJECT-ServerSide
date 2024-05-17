from .. import db
from sqlalchemy.sql import func


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    alias = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True, server_default='0')
    deleted_by = db.Column(db.Integer, nullable=True, server_default='0')
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')

    def __repr__(self):
        return '<Guest {}>'.format(self.name)
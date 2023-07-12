from .. import db
from sqlalchemy.sql import func

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_admin = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=True)
    expired_at = db.Column(db.BigInteger, nullable=False)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')

    def __repr__(self):
        return '<Auth {}>'.format(self.name)
from .. import db
from sqlalchemy.sql import func

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    update_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True, server_default='0')
    deleted_by = db.Column(db.Integer, nullable=True, server_default='0')
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)
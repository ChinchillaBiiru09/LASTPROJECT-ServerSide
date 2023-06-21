from .. import db
from sqlalchemy.sql import func

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    # created_by =  db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    # updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=False)
    # deleted_by = db.Column(db.Integer, nullable=False)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
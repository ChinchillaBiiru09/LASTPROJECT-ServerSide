from .. import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    last_active = db.Column(db.BigInteger, nullable=True) 
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by =  db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=False)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<User {}>'.format(self.name)
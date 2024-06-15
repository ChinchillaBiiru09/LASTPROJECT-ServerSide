from .. import db
from sqlalchemy.sql import func

""" 
    # EXAMPLE
    |   id    |   category    |           data            |   created_at  |   created_by  |   updated_at  |   updated_by  |   deleted_at  |   deleted_by  |   is_delete   |
    |  (int)  |    (sting)    |          (text)           |    (bigint)   |     (int)     |    (bigint)   |      (int)    |    (bigint)   |      (int)    |     (int)     |
    |---------|---------------|---------------------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
    |         |               |{"woman_name" : "required",|               |               |               |               |               |               |               |
    |    1    |  Pernikahan   | "man_name" : "required",  |    12345678   |       1       |    12345678   |       1       |    12345678   |       1       |       0       |
    |         |               | "address" : "optional" }  |               |               |               |               |               |               |               |
"""
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    format_data = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True, server_default='0')
    deleted_by = db.Column(db.Integer, nullable=True, server_default='0')
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)
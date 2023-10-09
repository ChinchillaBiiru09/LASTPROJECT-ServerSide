from .. import db
from sqlalchemy.dialects.mysql import LONGBLOB

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(75), nullable=False)
    file = db.Column(LONGBLOB(), nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Test {}>'.format(self.name)
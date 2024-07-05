from .. import db
from sqlalchemy.sql import func

class Greeting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Integer, nullable=False) # 1 : Hadir | 0 : Tidak Hadir
    message = db.Column(db.Text(), nullable=False)
    invitation_code = db.Column(db.String(5), nullable=False)
    user_id =  db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Greeting {}>'.format(self.name)
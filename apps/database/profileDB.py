from .. import db
from sqlalchemy.dialects.mysql import LONGBLOB

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    first_name = db.Column(db.String(75), nullable=False)
    middle_name = db.Column(db.String(75), nullable=True)
    last_name = db.Column(db.String(75), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    photos = db.Column(LONGBLOB(), nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Profile {}>'.format(self.name)
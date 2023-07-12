from .. import db
from sqlalchemy.sql import func
import time

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=True, server_default = str(int(round(time.time()*1000))))
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')

    def __repr__(self):
        return '<Log {}>'.format(self.name)
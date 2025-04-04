from .. import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    activity = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')

    def __repr__(self):
        return '<Log {}>'.format(self.name)
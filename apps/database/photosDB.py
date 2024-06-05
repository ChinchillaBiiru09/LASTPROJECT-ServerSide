from .. import db

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file = db.Column(db.Text(), nullable=False)
    file_name = db.Column(db.Text(), nullable=False)
    file_path = db.Column(db.Text(), nullable=False)
    status_file = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=True, server_default='0')
    
    def __repr__(self):
        return '<Photos {}>'.format(self.name)
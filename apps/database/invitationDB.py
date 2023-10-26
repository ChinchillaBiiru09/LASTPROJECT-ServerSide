from .. import db

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    category_id = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    wallpaper = db.Column(db.Text(), nullable=True)
    personal_data = db.Column(db.Text(), nullable=False)
    inv_setting = db.Column(db.Text(), nullable=True)
    code = db.Column(db.String(6), nullable=False)
    link = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Invitation {}>'.format(self.name)
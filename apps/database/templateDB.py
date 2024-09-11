from .. import db
# from sqlalchemy.dialects.mysql import LONGBLOB

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, server_default='0') # Admin [0] or other user [anything/user id]
    title = db.Column(db.String(150), nullable=False)
    thumbnail = db.Column(db.Text(), nullable=False)
    css_file = db.Column(db.Text(), nullable=False)
    js_file = db.Column(db.Text(), nullable=True)
    wallpaper = db.Column(db.Text(), nullable=True)
    wallpaper_2 = db.Column(db.Text(), nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    type = db.Column(db.Integer, nullable=False, server_default='0') # public [0] or private [1]
    used_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Template {}>'.format(self.name)
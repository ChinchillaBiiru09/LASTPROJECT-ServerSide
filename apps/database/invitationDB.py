from .. import db
""" 
    # EXAMPLE
    |   id    |   user_level    |           user_id            |   created_at  |   created_by  |   updated_at  |   updated_by  |   deleted_at  |   deleted_by  |   is_delete   |
    |  (int)  |    (sting)    |          (text)           |    (bigint)   |     (int)     |    (bigint)   |      (int)    |    (bigint)   |      (int)    |     (int)     |
    |---------|---------------|---------------------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
    |         |               |{"woman_name" : "required",|               |               |               |               |               |               |               |
    |    1    |  Pernikahan   | "man_name" : "required",  |    12345678   |       1       |    12345678   |       1       |    12345678   |       1       |       0       |
    |         |               | "address" : "optional" }  |               |               |               |               |               |               |               |
"""
class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    category_id = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    personal_data = db.Column(db.Text(), nullable=False)
    other_info = db.Column(db.Text(), nullable=True)
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
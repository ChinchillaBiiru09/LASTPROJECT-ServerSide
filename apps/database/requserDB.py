from .. import db
# from sqlalchemy.dialects.mysql import LONGBLOB

""" 
    # EXAMPLE
    |   id    |   category    |           data            |   created_at  |   created_by  |   updated_at  |   updated_by  |   deleted_at  |   deleted_by  |   is_delete   |
    |  (int)  |    (sting)    |          (text)           |    (bigint)   |     (int)     |    (bigint)   |      (int)    |    (bigint)   |      (int)    |     (int)     |
    |---------|---------------|---------------------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
    |         |               |{"woman_name" : "required",|               |               |               |               |               |               |               |
    |    1    |  Pernikahan   | "man_name" : "required",  |    12345678   |       1       |    12345678   |       1       |    12345678   |       1       |       0       |
    |         |               | "address" : "optional" }  |               |               |               |               |               |               |               |
"""
class Requser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_level = db.Column(db.Integer, nullable=False, comment="1 = Admin, 2 = User")
    category = db.Column(db.Integer, nullable=False)
    design_file = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    deadline = db.Column(db.BigInteger, nullable=False)
    type = db.Column(db.Text(), nullable=False, comment="0 = Public, 1 = Private")
    status = db.Column(db.Integer, nullable=False) # 0 = waiting | 1 = acc | 2 = proccess | 3 = decline | 4 = clear
    created_at = db.Column(db.BigInteger, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Req_User {}>'.format(self.name)
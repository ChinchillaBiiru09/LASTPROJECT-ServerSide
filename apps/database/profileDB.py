from .. import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
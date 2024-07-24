from db import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    origin_value = db.Column(db.Text, nullable=False)

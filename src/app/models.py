from flask import current_app
from app import db


class Restaurant(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(56), nullable=False)

    def __repr__(self):
        return f"Restaurant '{self.name}'"



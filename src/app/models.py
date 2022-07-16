from flask import current_app
from sqlalchemy.orm import backref
from app import db

class Address(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    street     = db.Column(db.String(256), nullable=True)
    city       = db.Column(db.String(256), nullable=True)
    st_number  = db.Column(db.String(16), nullable=True)

    def __repr__(self):
        return f"{self.street}, {self.st_number} - {self.city}"

class Info(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    main_dish_type      = db.Column(db.String(128), nullable=False)
    main_dish_price     = db.Column(db.Float(precision=2), nullable=False)
    main_dish_rate      = db.Column(db.Float(precision=2), nullable=True)
    average_rate        = db.Column(db.Float(precision=2), nullable=True)
    downtown_distance   = db.Column(db.Float(precision=16, decimal_return_scale=None), nullable=True)


class Restaurant(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(56), nullable=False)
    type       = db.Column(db.String(56), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)
    address    = db.relationship("Address", backref=backref("address", uselist=False))
    info_id    = db.Column(db.Integer, db.ForeignKey('info.id'), unique=True)
    info       = db.relationship("Info", backref=backref("info", uselist=False))

    def __repr__(self):
        return f"Restaurant '{self.name}' - {self.type} - {self.address}"



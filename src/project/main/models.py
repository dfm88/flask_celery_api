from flask import current_app
from sqlalchemy.orm import backref
from sqlalchemy import UniqueConstraint
from project import db


class Address(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    street        = db.Column(db.String(256), nullable=True)
    city          = db.Column(db.String(256), nullable=True)
    st_number     = db.Column(db.String(16), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id", ondelete='CASCADE'), unique=True, nullable=False)
    restaurant    = db.relationship(
        "Restaurant", back_populates="address", uselist=False)

    def __repr__(self):
        return f"{self.street}, {self.st_number} - {self.city}"


class Info(db.Model):
    id                       = db.Column(db.Integer, primary_key=True)
    tipo_piatto_principale   = db.Column(db.String(128), nullable=True)
    prezzo_piatto_principale = db.Column(db.Float(precision=2), nullable=True)
    voto_piatto_principale   = db.Column(db.Float(precision=2), nullable=True)
    voto_medio               = db.Column(db.Float(precision=2), nullable=True)
    distanza_dal_centro      = db.Column(
        db.Float(precision=16, decimal_return_scale=None), nullable=True)
    restaurant_id            = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id', ondelete='CASCADE'), unique=True, nullable=False)
    restaurant               = db.relationship(
        "Restaurant", back_populates="info", uselist=False)


class Restaurant(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'type', name='unique_rest_constraint'),
    )
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(56), nullable=False)
    type    = db.Column(db.String(56), nullable=False)
    # address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)
    address = db.relationship(
        "Address", back_populates="restaurant", uselist=False)
    # info_id    = db.Column(db.Integer, db.ForeignKey('info.id'), unique=True)
    info    = db.relationship("Info", back_populates="restaurant", uselist=False)

    def __repr__(self):
        return f"Restaurant '{self.name}' - {self.type} - {self.address}"

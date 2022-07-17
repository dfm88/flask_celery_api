import re

from flask_admin.contrib.sqla import ModelView

from project import db
from project.main.exceptions import InvalidAddressException


class Address(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    street        = db.Column(db.String(256), nullable=True)
    city          = db.Column(db.String(256), nullable=True)
    st_number     = db.Column(db.String(16), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id", ondelete='CASCADE'), unique=True, nullable=False)
    restaurant    = db.relationship(
        "Restaurant", back_populates="address", uselist=False)

    def __init__(self, address: str, *args, **kwargs):
        """
        address string should have format: 'street, street_number - city' 
        """
        try:
            address = re.split(r',|-', address)
            self.street = address[0].strip()
            self.st_number = address[1].strip()
            self.city = address[2].strip()
            super().__init__(*args, **kwargs)

        except InvalidAddressException as ex:
            raise ex


    def __repr__(self):
        return f"{self.street}, {self.st_number} - {self.city}"


class Info(db.Model):
    id                       = db.Column(db.Integer, primary_key=True)
    tipo_piatto_principale   = db.Column(db.String(256), nullable=True)
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
    name    = db.Column(db.String(256), nullable=False)
    type    = db.Column(db.String(256), nullable=False)
    address = db.relationship(
        "Address", back_populates="restaurant", uselist=False, cascade="all, delete-orphan")
    info    = db.relationship(
        "Info", back_populates="restaurant", uselist=False,cascade="all, delete-orphan")

    def __repr__(self):
        return f"Restaurant '{self.name}' - {self.type} - {self.address}"



class ChildView(ModelView):
    """
    Shows ref field of Restaurant in admin panel
    """
    column_display_pk = True
    column_hide_backrefs = False
    column_list = (
        'id', 
        'name',
        'type',
        'address',
        'info',
    )


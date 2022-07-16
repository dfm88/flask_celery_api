
from flask import Blueprint
from flask import request

from app.models import Address, Info, Restaurant
from app import db
import json
import re


main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@main.route('/add', methods=['POST'])
def add():
    import ipdb
    ipdb.set_trace()
    data = request.get_json()
    for el in data:
        name = el['name']
        type_ = el['type']

        address = el['address']
        address = re.split(r',|-', address)
        street = address[0].strip()
        st_number = address[1].strip()
        city = address[2].strip()

        info = el['info']

        address = Address(street=street, city=city, st_number=st_number)
        info = Info(**info)
        restaurant = Restaurant(name=name, type=type_)
        restaurant.address = address
        restaurant.info = info

        db.session.add(restaurant)
        db.session.commit()

    return json.dumps("Added"), 200


@main.route("/del/<int:rest_id>", methods=['POST'])
def delete_restaurant(post_id):
    res = Restaurant.query.get_or_404(post_id)

    db.session.delete(res)
    db.session.commit()
    return 'ok', 200

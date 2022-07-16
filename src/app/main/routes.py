
from flask import Blueprint
from flask import request

from app.models import Restaurant
from app import db
import json


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }



@main.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    name = data['name']
    restaurant = Restaurant(name=name)
    db.session.add(restaurant)
    db.session.commit()

    return json.dumps("Added"), 200
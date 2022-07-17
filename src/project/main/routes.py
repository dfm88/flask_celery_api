
import json

from celery.result import AsyncResult
from flask import Blueprint, jsonify
from flask import request

from project.main.tasks import func1
from project.main.models import Address, Info, Restaurant
from project import db
from project.main.utils import validate_data_to_model


main_blueprint = Blueprint(
    "main",
    __name__,
)

@main_blueprint.route('/', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@main_blueprint.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    validate_data_to_model(data_list=data)

    return json.dumps("Added"), 200


@main_blueprint.route("/del/<int:rest_id>", methods=['POST'])
def delete_restaurant(post_id):
    res = Restaurant.query.get_or_404(post_id)

    db.session.delete(res)
    db.session.commit()
    return 'ok', 200


@main_blueprint.route('/send', methods=['GET'])
def celery_func():
    task = func1.delay('ciao')
    return {
        'id': task.id
    }

@main_blueprint.route('/read/<task_id>')
def taskstatus(task_id):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'queue_state': task.state,
            'queue_results': task.result,
            'status': 'Process is ongoing...',
        }
    else:
        response = {
            'queue_state': task.state,
            'result': task.wait()
        }
    return jsonify(response)

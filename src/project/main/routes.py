
from celery.result import AsyncResult

from flask import Blueprint, jsonify, request

from project.main.models import Restaurant
from project import db
from project.main.tasks import validate_data_to_model


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
    job = validate_data_to_model.apply_async(
        kwargs={
            'data_list':data
        }
    )
    res = {
        'id': job.id
    }
    
    return jsonify(res)


@main_blueprint.route("/del/<int:rest_id>", methods=['DELETE'])
def delete_restaurant(rest_id):
    res = Restaurant.query.get_or_404(rest_id)

    db.session.delete(res)
    db.session.commit()
    db.session.close()
    return 'ok', 204


##########################
@main_blueprint.route('/task_status/<task_id>')
def taskstatus(task_id):
    task = AsyncResult(task_id)
    if isinstance(task.result, Exception):
        task_result = str(task.result)
    else:
        task_result = task.result

    response = {
        'state': task.state,
        'result': task_result,
    }

    return jsonify(response)

from flask import Blueprint


main_blueprint = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder=None
)


from . import models, tasks

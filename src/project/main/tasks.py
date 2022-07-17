import os
import traceback

from time import sleep
from typing import Tuple

from celery import shared_task, current_task, states
from celery.exceptions import Ignore
from celery.signals import worker_init

from project.main.exceptions import RestaurantAlreadyExists
from project.main.utils import validate_data

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# build celery-specific session
Session = scoped_session(
    sessionmaker(autocommit=True, autoflush=True)
)

@worker_init.connect
def initialize_session(*args, **kwargs):
    """
    Initialize Celery session on startup
    """
    some_engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))    
    Session.configure(bind=some_engine)

@shared_task
def validate_data_to_model(data_list: list) -> dict:
    session = Session
    data_length = len(data_list)
    added = 0
    result = {
        'total': data_length,
        'added': 0,
    }
    with session.begin():
        for i, el in enumerate(data_list):
            try:
                meta = {
                    'status': '..working..',
                    'parsed': i+1,
                    'to_parse': data_length
                }
                current_task.update_state(
                    state=states.PENDING,
                    meta=meta
                )
                print(f'Parsing {i+1}/{data_length}')
                validate_data(data=el, session=session)
                result['added'] += 1
            except RestaurantAlreadyExists as rex:
                print(rex)
                continue
            except Exception as ex:
                print(f'Error saving data {el}: \n{ex}')
                current_task.update_state(
                    state=states.FAILURE,
                    meta={
                        'exc_message': traceback.format_exc().split('\n'),
                        'exc_type': type(ex).__name__,
                    }
                )
                raise Ignore()

    return result
from typing import Tuple
from project import db
from sqlalchemy.orm.exc import NoResultFound
from psycopg2 import IntegrityError
from project.main.exceptions import RestaurantAlreadyExists
from project.main.models import Address, Info, Restaurant




def validate_data(data: dict, session) -> Tuple[Restaurant, Address, Info]:
    # RESTAURANT
    restaurant = _save_restaurant(
        data=data,
        session=session,
    )

    # ADDRESS
    address_get = {
        'restaurant': restaurant,
    }
    address_create = {
        'restaurant': restaurant,
        'address': data.get('address'),
    }
    address = get_or_create(
        session=session,
        model=Address,
        model_get_kwargs=address_get,
        model_create_kwargs=address_create
    )

    # INFO
    info_get = {
        'restaurant': restaurant,
    }
    info_create = {
        'restaurant': restaurant,
        **data.get('info', {})
    }
    info = get_or_create(
        session=session,
        model=Info,
        model_get_kwargs=info_get,
        model_create_kwargs=info_create
    )

    return (
        restaurant,
        address,
        info,
    )


def _save_restaurant(data: dict, session: db.session) -> Restaurant:
    restaurant_dict = {}
    restaurant_dict['name'] = data.get('name')
    restaurant_dict['type'] = data.get('type')

    restaurant, created = get_or_create(
        session,
        model=Restaurant,
        model_get_kwargs=restaurant_dict,
        model_create_kwargs=restaurant_dict,
    )

    if not created:
        raise RestaurantAlreadyExists(
            'Restaurant %s - %s already exists' % (
                restaurant.name,
                restaurant.type
            )
        )

    return restaurant


def get_or_create(
    session,
    model,
    model_get_kwargs=None,
    model_create_kwargs=None,
) -> Tuple[db.Model, bool]:
    try:
        model_get_kwargs = model_get_kwargs or {}
        model_create_kwargs = model_create_kwargs or {}
        return session.query(model).filter_by(**model_get_kwargs).one(), False
    except NoResultFound:
        instance = model(**model_create_kwargs)
        try:
            session.add(instance)
            # session.commit() # under transaction
            return instance, True
        except IntegrityError:
            # in case of race condition (element added
            # between verifying existence and creation)
            session.rollback()
            return session.query(model).filter_by(**model_get_kwargs).one(), False

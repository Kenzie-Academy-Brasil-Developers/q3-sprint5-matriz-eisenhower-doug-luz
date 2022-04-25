from http import HTTPStatus

from app.configs.database import db
from app.models.category_model import CategoryModel
from flask import current_app, jsonify, request
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_category():
    data = request.get_json()
    data['name']=data['name'].title()
    category = CategoryModel(**data)

    session: Session = db.session()

    try:    
        session.add(category)
        session.commit()

        return jsonify(category), HTTPStatus.CREATED
    except IntegrityError as e:
        if type(e.orig == UniqueViolation):
            return {'Error':'Category already exists'}, HTTPStatus.CONFLICT

def retrieve():
    session:Session = current_app.db.session

    categories = session.query(CategoryModel).all()
    if not categories:
        return{'Error':'There are no category on database'}, HTTPStatus.BAD_REQUEST
    
    print(categories)
    print('**************************************',type(categories))
    session.add(categories[0])
    session.commit()

    return jsonify(categories), HTTPStatus.OK

def upgrade(_id:int):
    data = request.get_json()

    session:Session = current_app.db.session

    category = session.query(CategoryModel).get(_id)

    if not category:
        return {'Error':'Id not found'}, HTTPStatus.BAD_REQUEST

    for key, value in data.items():
        setattr(category, key, value)

    session.commit()

    return jsonify(category), HTTPStatus.OK
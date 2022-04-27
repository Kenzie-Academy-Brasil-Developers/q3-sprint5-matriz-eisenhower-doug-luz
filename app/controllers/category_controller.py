from dataclasses import asdict
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

    categories_list = session.query(CategoryModel).order_by(CategoryModel._id).all()
    if categories_list == []:
        return{'Error':'There are no category on database'}, HTTPStatus.NOT_FOUND
    result = []
    for category in categories_list:
        category_dict = asdict(category)
        category_dict['tasks']=[{
            "_id":cat._id,
            "name":cat.name,
            "description":cat.description,
            "duration":cat.duration,
            "classification":cat.eisenhower.type
            } for cat in category.tasks]
        result.append(category_dict)    
    

    return jsonify(result), HTTPStatus.OK

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

def delete(_id:int):
    session:Session = current_app.db.session

    category = session.query(CategoryModel).get(_id)

    if not category:
        return {'Error': 'Id not found'}, HTTPStatus.NOT_FOUND

    session.delete(category)
    session.commit()

    return '', HTTPStatus.NO_CONTENT
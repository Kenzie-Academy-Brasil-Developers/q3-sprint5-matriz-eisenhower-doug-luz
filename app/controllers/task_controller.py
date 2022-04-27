from genericpath import exists
from http import HTTPStatus
from app.models.category_model import CategoryModel
from app.models.task_model import TaskModel
from flask import current_app, jsonify, request
from sqlalchemy.orm import Session
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_task():
    session:Session = current_app.db.session
    data = request.get_json()
    
    if data['urgency'] > 2 or data['importance'] > 2:
        expected = {'importance': [1,2],'urgency': [1,2] }
        received = {'importance': data['importance'], 'urgency': data['urgency']}
        return {'msg': {"valid_options":expected, "received_options":received}}, HTTPStatus.BAD_REQUEST
    
    if data['importance']==data['urgency']==1:
        data['eisenhower_id'] = 1
    if data['importance']==2 and data['urgency']==1:
        data['eisenhower_id'] = 2
    if data['importance']==1 and data['urgency']==2:
        data['eisenhower_id'] = 3
    if data['importance']==2 and data['urgency']==2:
        data['eisenhower_id'] = 4
    
    categories = data.pop('categories')
    normalized_categories = [category.title() for category in categories]

    try:
        task = TaskModel(**data)

        for category in normalized_categories:
            existent_category = session.query(CategoryModel).filter_by(name=category).first()
            if not existent_category:
                new_category = CategoryModel(name=category)
                session.add(new_category)
                task.categories.append(new_category)
            else:
                task.categories.append(existent_category)

        session.add(task)
        session.commit()
        return {
            '_id':task._id,
            'name':task.name,
            'description':task.description,
            'duration':task.duration,
            'classification':task.eisenhower.type,
            'categories':normalized_categories
        }
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {'Error':'Name already exists'}, HTTPStatus.CONFLICT

def upgrade(_id:int):
    session:Session = current_app.db.session
    data = request.get_json()

    task = session.query(TaskModel).get(_id)
    print('*'*80,task.__dict__)

    if not task:
        return {'Error':'Id not found'}, HTTPStatus.BAD_REQUEST
    
    cat = data.get('categories', False)
    if cat:
        print(cat)
        categories = [d.title() for d in data.pop('categories')]
        task.categories=categories
    else:
        cats = []
        x= enumerate(task.categories)
        for y in x:
            cats.append(y[1].name)
    # normalized_categories = [category.title() for category in categories]
    
    if data['importance']==data['urgency']==1:
        data['eisenhower_id'] = 1
    if data['importance']==2 and data['urgency']==1:
        data['eisenhower_id'] = 2
    if data['importance']==1 and data['urgency']==2:
        data['eisenhower_id'] = 3
    if data['importance']==2 and data['urgency']==2:
        data['eisenhower_id'] = 4
       
    data['name']=data['name'].title()
    try:
          
        for key, value in data.items():
            setattr(task, key, value)
       # session.add(task)
        session.commit()
        print(task._id, task.description)
        return {
                '_id':task._id,
                'name':task.name,
                'description':task.description,
                'duration':task.duration,
                'classification':task.eisenhower.type,
                'categories': cats
            }, HTTPStatus.OK   

    except IntegrityError as e:
        if type(e.orig)== UniqueViolation:
            return {'Error':'Name already exists'}, HTTPStatus.CONFLICT


def delete(_id:int):
    session:Session = current_app.db.session

    task = session.query(TaskModel).get(_id)
    if not task:    
        return {'Error': 'Id not found'}, HTTPStatus.NOT_FOUND
    
    session.delete(task)
    session.commit()

    return '', HTTPStatus.NO_CONTENT


def retrieve():
    session:Session = current_app.db.session


    category_list = session.query(CategoryModel).all()
    
    

    
    
    # task_list=[]
    # for task in tasks:
    #     task_list.append({
    #         '_id':task._id,
    #         'name':task.name,
    #         'description':task.description,
    #         'duration':task.duration,
    #         # 'classification':task.eisenhower.type,
    #         'categories': cats
    #     })
    
    return (category_list), HTTPStatus.OK
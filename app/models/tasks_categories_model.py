from app.configs.database import db

tasks_categories = db.Table(
    'tasks_categories',
    db.Column('_id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks._id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories._id'))
)

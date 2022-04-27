from app.configs.database import db
from sqlalchemy import Column, ForeignKey, String, Integer, Text

from app.models.eisenhower_model import EisenhowerModel
from dataclasses import dataclass

@dataclass
class TaskModel(db.Model):
    _id:int
    name:str
    description:str
    duration:int
    #eisenhower:str

    __tablename__='tasks'

    _id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)

    eisenhower_id = Column(Integer, ForeignKey('eisenhower._id'), nullable=False)

    eisenhower = db.relationship('EisenhowerModel', backref='tasks')
    


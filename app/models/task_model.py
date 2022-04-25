from app.configs.database import db
from sqlalchemy import Column, ForeignKey, String, Integer, Text

from app.models.eisenhower_model import EisenhowerModel

class TaskModel(db.Model):
    __tablename__='tasks'

    _id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    diration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)

    eisenhower_id = Column(Integer, ForeignKey('eisenhower._id'), nullable=False)

    


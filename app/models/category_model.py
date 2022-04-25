from app.configs.database import db
from sqlalchemy import Column, Text, Integer, String
from dataclasses import dataclass

@dataclass
class CategoryModel(db.Model):
    __tablename__ = 'categories'
    _id:int
    name:str
    description:str


    _id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
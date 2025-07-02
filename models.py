from sqlalchemy import Column, Integer, String
from static.db import db

# define model
class Link(db.Model):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)

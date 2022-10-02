from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy.types import String, Integer, Text
from sqlalchemy.schema import Column

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key = True, index=True)
    nickname = Column(String(30), unique=True)
    fullname = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(Text())

    items = relationship("Item", back_populates='owner')


class Item(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500), index=True)
    price = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates='items')
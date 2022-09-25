from pydantic import BaseModel
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
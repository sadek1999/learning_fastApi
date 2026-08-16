from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    is_completed=Column(Boolean)
    owner_todo=Column(Integer,ForeignKey("users.id"))

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    username=Column(String, unique=True)
    email=Column(String, unique=True)
    password=Column(String)
    user_role=Column(String)
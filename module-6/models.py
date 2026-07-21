from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    is_completed=Column(Boolean)
    owner_todo=Column(int,ForeignKey("users.id"))


class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    name=Column(String,unique=True)
    hash_password= Column(String)
    is_active=Column(bool,default=True)   
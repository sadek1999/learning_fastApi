from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, sessionLocal
from models import Todo



app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()  
db_dependency=Annotated[Session, Depends(get_db)]

@app.get('/')
def get_todos(db: db_dependency): 
    return db.query(Todo).all()

@app.get('/todo/{todo_id}')
def get_todos(db: db_dependency, todo_id:int): 
    return db.query(Todo).filter(Todo.id == todo_id).first()
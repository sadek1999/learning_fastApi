from contextlib import asynccontextmanager
from typing import Annotated,Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse

from database import engine, sessionLocal
from models import Base, Todo

from router import auth 



app = FastAPI()

class Todos(BaseModel):
    id :int
    title: str =Field(max_length=10)
    description : str =Field(max_length=100)
    priority: int=Field(gt=0, le=6)
    is_completed:bool=False

class UpdateTodos(BaseModel):
    title: Optional[str] = Field(default=None, max_length=10)
    description: Optional[str] = Field(default=None, max_length=100)
    priority: Optional[int] = Field(default=None, gt=0, le=6)
    is_completed: Optional[bool] = False


Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

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
def get_todos_by_id(db: db_dependency, todo_id:int): 
    t = db.query(Todo).filter(Todo.id == todo_id).first()
    if t is not None:
        return t
    else:
        raise HTTPException(status_code=404, detail="Todo is not found")
    


@app.post('/create')
def crate_todos(db: db_dependency, new_todo:Todos): 
    todo_model= Todo(**new_todo.model_dump())  
    db.add(todo_model)
    db.commit()  
    return JSONResponse(status_code=201,content={"message":"todo created successfully"})


@app.put('/update/{todo_id}')
def update_todo(db: db_dependency, todo_id:int, update_todo:UpdateTodos): 
    t = db.query(Todo).filter(Todo.id == todo_id).first()
    if t is  None:
      raise HTTPException(status_code=404, detail="Todo is not found")
    
    update_data=update_todo.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(t,key,value)

    db.commit()
    return JSONResponse(status_code=200,content={"message":"todo updated successfully"})
    


@app.delete('/update/{todo_id}')
def delete_todo(db: db_dependency, todo_id:int): 
    t = db.query(Todo).filter(Todo.id == todo_id).first()
    if t is  None:
      raise HTTPException(status_code=404, detail="Todo is not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()

    db.commit()
    return JSONResponse(status_code=200,content={"message":"todo deleted successfully"})        
    
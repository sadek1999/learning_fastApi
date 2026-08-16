
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db 
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
import app.models as models
from app.models import Todo,User
from app.schemas import TodoBase 



app =FastAPI()

Base.metadata.create_all(bind=engine)

db_dependency=Annotated[Session, Depends(get_db)]



@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI application!"}


# - todo api --

@app.post("/todos")
def create_todo(new_todo:TodoBase , db: db_dependency):
    todo_model=Todo(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return JSONResponse(status_code=201, content={"message": "Todo created successfully", "todo_id": todo_model.id})

@app.get("/todos")
def read_todos(db: db_dependency):
    todos=db.query(Todo).all()
    return JSONResponse(status_code=200, content={"todos": todos})

@app.get("/todo/{todo_id}")
def read_todo_by_id():
    pass

@app.put("/todo/{todo_id}")
def update_todo_by_id():
    pass

@app.delete("/todo/{todo_id}")
def delete_todo_by_id():
    pass


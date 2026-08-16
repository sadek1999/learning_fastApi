
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db 
from fastapi import Depends, FastAPI,status,HTTPException
from fastapi.responses import JSONResponse
import app.models as models
from app.models import Todo,User
from app.schemas import TodoBase, TodoResponse,TodoUpdate,UserBase,UserResponse
from sqlalchemy.exc import SQLAlchemyError



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
    return db.query(Todo).all()  


@app.get("/todos/{todo_id}",response_model=TodoResponse ,
         status_code=status.HTTP_200_OK)
def read_todo_by_id(todo_id:int, db:db_dependency):
     todo=db.query(Todo).filter(Todo.id == todo_id).first()
     if todo is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found ")

     return todo


@app.delete("/todo/{todo_id}")
def delete_todo_by_id(todo_id:int, db:db_dependency):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found ")

    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    return JSONResponse(status_code=status.HTTP_301_MOVED_PERMANENTLY ,content={"message":"deleted "})


@app.patch("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_by_id(todo_id: int, update_todo: TodoUpdate, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    update_data = update_todo.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided to update")

    for key, value in update_data.items():
        setattr(todo, key, value)

    try:
        db.commit()
        db.refresh(todo)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update todo")

    return todo


# -----------------------User Api ----------------------


@app.post("/users")
def create_users(db:db_dependency,new_user:UserBase):
    data=User(**new_user.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return JSONResponse(status_code=201, content={"message": "Todo created successfully", "todo_id": data.id})


@app.get("/users")
def get_all_users(db:db_dependency):
    return db.query(User).all()


@app.get("/users/{user_id}")
def get_users_by_id(user_id:int,db:db_dependency):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not Found ")

    return user


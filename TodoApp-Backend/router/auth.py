from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from database import sessionLocal
from models import Users

router = APIRouter()

# Initialize modern password hasher
password_hash = PasswordHash.recommended()


class CreateUser(BaseModel):
    email: EmailStr  # EmailStr validates that input is a valid email
    name: str
    role: str
    password: str

def authenticate_user(username, password, db):
    user=db.query(Users).filter(Users.name == username).first()
    if user is None:
        return False

    if password_hash.verify(password=password,hash=user.hash_password):
        return True

    return True



# Database dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create_user")
def create_user(db: db_dependency, new_user: CreateUser):
    # # Check if user already exists
    # existing_user = (
    #     db.query(Users).filter(Users.email == new_user.email).first()
    # )
    # if existing_user:
    #     raise HTTPException(
    #         status_code=400, detail="User with this email already exists"
    #     )

    # Hash the password and save to DB
    user_model = Users(
        email=new_user.email,
        name=new_user.name,
        role=new_user.role,
        hash_password=password_hash.hash(new_user.password),
    )
    db.add(user_model)
    db.commit()

    return JSONResponse(
        status_code=201, content={"message": "User created successfully"}
    )


@router.post("/login")
def user_login(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    

   user = authenticate_user(
       username=form_data.username,
       password=form_data.password,
       db=db)


   if user :
       return "Authenticated user " 
   else:
       return "Unknown user ......"

  

    # # Check if user exists and password is correct
    # if not user or not password_hash.verify(
    #     form_data.password, user.hash_password
    # ):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # return {
    #     "message": "Login successful",
    #     "user_id": user.id if hasattr(user, "id") else None,
    #     "email": user.email,
    # }

   
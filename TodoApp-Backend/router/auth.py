from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone
import jwt
from jwt.exceptions import PyJWTError


from database import sessionLocal
from models import Users

router = APIRouter()

# Initialize modern password hasher
password_hash = PasswordHash.recommended()

# Database dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


SECRET_kEY = "42dfa3488f48a7ff1c2207b95ded6acd2ab4a7589d0654f5ff56970ef8b13017"
ALGORITHM = "HS256"
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
        access_token=create_access_token(user.name,user.id,timedelta(minutes=40))
        return access_token

    return False


def create_access_token(user_name: str,user_id: int,expire_delta:timedelta):
    encode={'sub':user_name,'id': user_id}
    expires=datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expires})
    return jwt.encode(encode,SECRET_kEY,algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_kEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        user_id: int = payload.get("id")

       
        if user_name is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token claims")
            
        return {"user": user_name, "id": user_id}
        
    except PyJWTError: # Only catch JWT-related errors!
        raise HTTPException(
            status_code=401, 
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )



@router.post("/create_user")
def create_user(db: db_dependency, new_user: CreateUser):
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
    

   token = authenticate_user(
       username=form_data.username,
       password=form_data.password,
       db=db)


   if token :
        return {"access_token": token, "token_type": "bearer"}
   else:
       return "Unknown user ......"

  

    

   
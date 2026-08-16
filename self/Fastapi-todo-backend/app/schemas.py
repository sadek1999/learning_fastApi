

from typing import Optional

from pydantic import BaseModel, Field,ConfigDict,EmailStr



class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, examples=["Finish FastAPI Project"])
    description: Optional[str] = Field(None, max_length=500, examples=["Implement models and routes"])
    priority: int = Field(..., ge=1, le=5, description="Priority level from 1 (low) to 5 (high)", examples=[3])
    is_completed: bool = Field(default=False, examples=[False])

    
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, examples=["Finish FastAPI Project"])
    description: Optional[str] = Field(None, max_length=500, examples=["Implement models and routes"])
    priority: Optional[int] = Field(None, ge=1, le=5, description="Priority level from 1 (low) to 5 (high)", examples=[3])
    is_completed: Optional[bool] = Field(None, examples=[False])


class TodoResponse(TodoBase):
  
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username of the user",
        examples=["sadek123"]
    )

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["sadek@example.com"]
    )

    password: str = Field(
        ...,
        description="User's password",
        examples=["StrongPassword123"]
    )

    user_role: str = Field(
        default="user",
        description="Role assigned to the user",
        examples=["user"]
    )


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
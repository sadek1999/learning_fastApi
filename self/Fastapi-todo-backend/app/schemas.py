

from typing import Optional

from pydantic import BaseModel, Field,ConfigDict



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
    
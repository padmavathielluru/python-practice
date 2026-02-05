from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    email:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        orm_mode=True
class TaskCreate(BaseModel):
    title:str
    user_id:int

class TaskUpdate(BaseModel):
    status:str


class TaskResponse(BaseModel):
    id:int
    tittle:str
    status:str
    user_id:int

    class Config:
        orm_model=True
        
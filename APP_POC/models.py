from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True)
    is_deleted = Column(Boolean, default=False) #for soft delete users


class Task(Base):
    __tablename__="tasks"

    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    status=Column(String,default="pending")
    user_id=Column(Integer,ForeignKey("users.id"))


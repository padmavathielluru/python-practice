from sqlalchemy.orm import Session
from models import User,Task
from fastapi import HTTPException

#function for reading  user details here
def get_users(db:Session):
    return db.query(User).all()

#function for reading tasks
def get_all_tasks(db:Session):
    return db.query(Task).all()

#function to read updated tasks by user id
def get_tasks_by_user(db:Session,user_id:int):
    return db.query(Task).filter(Task.user_id==user_id).all()

#function for creating user 
def create_user(db:Session,name:str,email:str):
    user=User(name=name,email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#function for creating a tasktable
def create_task(db:Session,title:str,user_id:str):
    task=Task(title=title,user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


#for updatiing the task 
def update_task(db:Session,task_id:int,status:str):
    task=db.query(Task).filter(Task.id==task_id).first()

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    task.status=status
    db.commit()
    return task

#for deleting the task
def delete_task(db:Session,task_id:int):
    task=db.query(Task).filter(Task.id==task_id).first()
    db.delete(task)
    db.commit()
#for doing soft delete
def soft_delete_user(db:Session,user_id:int):
    user=db.query(User).filter(User.id==user_id,User.is_deleted==False).first()

    if not user:
        return None
    user.is_deleted=True
    db.commit()
    return user



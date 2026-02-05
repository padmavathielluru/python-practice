from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal,engine
from crud import soft_delete_user

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#user API
@app.post("/users")
def create_user(
    user:schemas.UserCreate,
    db:Session=Depends(get_db)
    ):
    return crud.create_user(db,user.name,user.email)

@app.get("/users")
def get_users(db:Session=Depends(get_db)):
    return crud.get_users(db)

@app.get("/tasks")
def get_tasks(db:Session=Depends(get_db)):
    return crud.get_all_tasks(db)

@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id:int,db:Session=Depends(get_db)):
    return crud.get_tasks_by_user(db,user_id)

#task API
@app.post("/tasks")
def create_task(task:schemas.TaskCreate
                ,db:Session=Depends(get_db)
                ):
    return crud.create_task(db,task.title,task.user_id)

@app.put("/tasks/{task_id}")
def update_task(
    task_id:int,
    task:schemas.TaskUpdate,
    db:Session=Depends(get_db)
    ):

    return crud.update_task(db,task_id,task.status)

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,db:Session=Depends(get_db)):
    crud.delete_task(db,task_id)
    return{
        "message":"Task Deleted successfully"
    }

@app.delete("/users/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    user = soft_delete_user(db,user_id)
    if not user:
        raise HTTPException(status_code=404,details="user not found")
    
    return {
        "message":"user soft deleted successfully"
    }
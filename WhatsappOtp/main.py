from fastapi import FastAPI,Depends
from auth import router
from dotenv import load_dotenv
from utils import get_current_user

load_dotenv()

app=FastAPI()

app.include_router(router,prefix="/auth")


@router.get("/me")
def my_profile(current_user: str = Depends(get_current_user)):
    return {
        "phone": current_user,
        "status": "Logged in"
    }

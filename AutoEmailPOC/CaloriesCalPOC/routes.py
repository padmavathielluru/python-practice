from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services import calculate_bmr,calculate_daily_calories,calculate_bmi,bmi_category

router=APIRouter()
templates=Jinja2Templates(directory="templates")

@router.get("/",response_class=HTMLResponse)
def form(request:Request):
    return templates.TemplateResponse("form.html",{"request":request})

@router.post("/calculate",response_class=HTMLResponse)
def calculate(request:Request,
              age:int=Form(...),
              weight:float=Form(...),
              height:float=Form(...),
              gender:str=Form(...),
              activity:float=Form(...)
              ):
    
    bmr=calculate_bmr(age,weight,height,gender)
    daily_calories=calculate_daily_calories(bmr,activity)
    bmi=calculate_bmi(weight,height)
    category=bmi_category(bmi)

    return templates.TemplateResponse("result.html",{
        "request":request,
        "calories":round(daily_calories,2), #round(number, digits)
        "bmi":round(bmi,2),
        "category":category
    })
from fastapi import FastAPI,Depends,Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import Hmodels #to import my models file
import Hschemas #to import my schemas file
from Hdatabase import engine,SessionLocal,Base


Base.metadata.create_all(bind=engine)

app=FastAPI()
templates=Jinja2Templates(directory="Htemplates")

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()

#to check vital status
def check_status(hr,spo2,temp):
    #if heart rate is more than 130,oxygen<90,and temperature is more than 102 ,assigned this as a CRITICAL condition of that patient
    if hr>130 or spo2<90 or temp>102: 
        return "CRITICAL"
    #if heart rate is more than 100,oxygen<94,and temperature is more than 100 ,assigned this as a WARNING condition of that patient
    elif hr>100 or spo2<94 or temp>100:
        return "WARNING"
    else:
        return "NORMAL"
    
#recieve vitals API
@app.post("/vitals")
def receive_vitals(vital:Hschemas.VitalCreate,db:Session=Depends(get_db)):
    status=check_status(vital.heart_rate,vital.spo2,vital.temperature)

    #craeting database object here
    db_vital=Hmodels.Vital(
        patient_id=vital.patient_id,
        heart_rate=vital.heart_rate,
        spo2=vital.spo2,
        temperature=vital.temperature,
        status=status
    )
    db.add(db_vital)
    db.commit()
    db.refresh(db_vital)

    return {
        "message":"Vital stored","status":status
    }

@app.get("/",response_class=HTMLResponse)
def dashboard(request:Request,db:Session=Depends(get_db)):
    vitals=db.query(Hmodels.Vital).order_by(Hmodels.Vital.timestamp.desc()).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request":request,
         "vitals":vitals}
    )
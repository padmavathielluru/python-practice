from pydantic import BaseModel

class VitalCreate(BaseModel):
    patient_id:str
    heart_rate:float
    spo2:float
    temperature:float
    
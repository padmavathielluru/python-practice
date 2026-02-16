from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime
from Hdatabase import Base

class Vital(Base):
    __tablename__="vitals"

    id=Column(Integer,primary_key=True,index=True)
    patient_id=Column(String)
    heart_rate=Column(Float)
    spo2=Column(Float)
    temperature=Column(Float)
    status=Column(String)
    timestamp=Column(DateTime,default=datetime.now)


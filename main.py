from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the client')]
    gender: Annotated[Literal['male','female','other'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in Kgs')]

    @computed_field
    @property   
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


@app.get("/")
def hello():
    return {'message':'Hello World'}

@app.get("/info")
def info():
    return {'message':'This is the info about this app'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.post("/create")
def create_patient(patient: Patient):

    #load the existing data
    data = load_data()

    #check if the patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    #add new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

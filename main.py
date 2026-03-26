from fastapi import FastAPI, Path , HTTPException, Query #path is used to give description to the path parameter in the endpoint
import json

from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

class patient(BaseModel):
    id: Annotated[str, Field(..., description= 'id of the patient', example= 'P001')]
    name: Annotated[str, Field(..., description= 'name of the patient', example= 'John Doe')]
    city: Annotated[str, Field(..., description= 'city of the patient', example= 'New York')]
    age: Annotated[int, Field(...,gt=0, lt=120, description= 'age of the patient', example= 30)]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description= 'gender of the patient', example= 'Male')]
    height: Annotated[float,Field(...,gt=0, description= 'height of the patient', example= 175.5)]
    weight: Annotated[float, Field(...,gt=0, description= 'weight of the patient', example= 70.0)]

    @computed_field
    @property   
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)        
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        
class patientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description= 'name of the patient', example= 'John Doe')]
    city: Annotated[Optional[str], Field(default=None, description= 'city of the patient', example= 'New York')]
    age: Annotated[Optional[int], Field(default=None, description= 'age of the patient', example= 30)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None, description= 'gender of the patient', example= 'Male')]
    height: Annotated[Optional[float],Field(default=None, description= 'height of the patient', example= 175.5)]
    weight: Annotated[Optional[float], Field(default=None,gt=0, description= 'weight of the patient', example= 70.0)]

        

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)
    
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello():
    return {"message":"Patient management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by (e.g., name, age)"), order:str = Query("asc")):
    valid_fields = ["height", "weight", "bmi"]
    data = load_data()
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: asc, desc")
    
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    return sorted_data


@app.post('/create')
def create_patient(patient: patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code= 400, detail="Patient with this ID already exists")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: patientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient_data = data[patient_id]
    # Get only updated fields
    updated_data = patient_update.model_dump(exclude_unset=True)
    # Merge old + new data
    merged_data = {**existing_patient_data, **updated_data, "id": patient_id}
    # Validate using Pydantic model
    patient_obj = patient(**merged_data)
    # Save validated data (excluding id if needed)
    data[patient_id] = patient_obj.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(
        content={"message": "Patient updated successfully"},
        status_code=200
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)
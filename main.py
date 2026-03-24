from fastapi import FastAPI, Path , HTTPException, Query #path is used to give description to the path parameter in the endpoint
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

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
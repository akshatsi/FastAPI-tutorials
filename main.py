from fastapi import FastAPI
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
#from turtle import title

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated  # for type hinting and validation

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name", description="Patient's name")] # name must be a string with a maximum length of 50 characters
    email: EmailStr
    Linkedin: AnyUrl
    age: int
    weight: float = Field(gt=0) # weight must be greater than 0
    married: bool = False 
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
patients_info = {'name':'akshat', 'email': 'akshat@example.com', 'Linkedin': 'https://www.linkedin.com/in/akshat', 'age': 21, 'weight': 70.5, 'married': False, 'allergies': ['peanuts', 'pollen'], 'contact_details': {'email': 'akshat@example.com', 'phone': '123-456-7890'}}
patient1 = Patient(**patients_info)

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.Linkedin)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted data")

insert_patient_data(patient1)
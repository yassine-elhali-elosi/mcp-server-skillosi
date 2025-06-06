from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json

class EmployeeItem(BaseModel):
    id: Optional[int] = None
    firstName: str
    lastName: str
    currentWorkLocation: str
    service: str

SKILLOSI_DATA = {}
with open("database_sample.json", "r") as file:
    SKILLOSI_DATA = json.load(file)

EMPLOYEES_DICT = {item['id']: item for item in SKILLOSI_DATA}

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}

@app.get("/skillosi")
def get_all_employees():
    """
    Get all employees.
    """
    return SKILLOSI_DATA

@app.get("/skillosi/{employee_id}")
def get_employee_by_id(employee_id: int):
    """
    Get an employee by ID.
    """
    if employee_id not in EMPLOYEES_DICT:
        return {"error": "id not found."}
    return EMPLOYEES_DICT[employee_id]

@app.post("/skillosi")
def create_employee(employee: EmployeeItem):
    """
    Create a new employee.
    If the ID is not provided, it will be auto-generated.
    Args:
        item (EmployeeItem): The employee data to create.
    Format:
        {
            "firstName": "John",
            "lastName": "Doe",
            "currentWorkLocation": "New York",
            "service": "Engineering"
        }
    """
    if employee.id is None:
        employee.id = max(EMPLOYEES_DICT.keys()) + 1 if EMPLOYEES_DICT else 1
        
    employee_item = employee.model_dump()
    EMPLOYEES_DICT[employee.id] = employee_item
    SKILLOSI_DATA.append(employee_item)
    return employee_item

@app.put("/skillosi/{skillosi_id}")
def update(skillosi_id: int, employee: EmployeeItem):
    if skillosi_id not in EMPLOYEES_DICT:
        return {"error": "employee id not found."}
    
    employee_item = employee.model_dump()
    employee_item["id"] = skillosi_id
    EMPLOYEES_DICT[skillosi_id] = employee_item
    
    for i, element in enumerate(SKILLOSI_DATA):
        if element["id"] == skillosi_id:
            SKILLOSI_DATA[i] = employee_item
            break
    
    return employee_item

@app.delete("/skillosi/{employee_id}")
def delete(employee_id: int):
    if employee_id not in EMPLOYEES_DICT:
        return {"error": "id not found."}
    
    EMPLOYEES_DICT.pop(employee_id)
    SKILLOSI_DATA[:] = [employee for employee in SKILLOSI_DATA if employee["id"] != employee_id]
    
    return {"deleted": employee_id}

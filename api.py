from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json

class SkillositItem(BaseModel):
    id: Optional[int] = None
    firstName: str
    lastName: str
    currentWorkLocation: str
    service: str

SKILLOSI_DATA = {}
with open("skillosi_data.json", "r") as file:
    SKILLOSI_DATA = json.load(file)

SKILLOSI_DICT = {item['id']: item for item in SKILLOSI_DATA}

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}

@app.get("/skillosi")
def get_all_employees():
    """
    Fetch all Skillosi employees.
    """
    return SKILLOSI_DATA

@app.get("/skillosi/{skillosi_id}")
def get_employee_by_id(skillosi_id: int):
    """
    Fetch a Skillosi employee by ID.
    """
    if skillosi_id not in SKILLOSI_DICT:
        return {"error": "id not found."}
    return SKILLOSI_DICT[skillosi_id]

@app.post("/skillosi")
def create_employee(item: SkillositItem):
    """
    Create a new Skillosi employee.
    If the ID is not provided, it will be auto-generated.
    Args:
        item (SkillositItem): The Skillosi employee data to create.
    Format:
        {
            "firstName": "John",
            "lastName": "Doe",
            "currentWorkLocation": "New York",
            "service": "Engineering"
        }
    """
    if item.id is None:
        item.id = max(SKILLOSI_DICT.keys()) + 1 if SKILLOSI_DICT else 1
        
    item_dict = item.model_dump()
    SKILLOSI_DICT[item.id] = item_dict
    SKILLOSI_DATA.append(item_dict)
    return item_dict

@app.put("/skillosi/{skillosi_id}")
def update(skillosi_id: int, item: SkillositItem):
    if skillosi_id not in SKILLOSI_DICT:
        return {"error": "id not found."}
    
    item_dict = item.model_dump()
    item_dict["id"] = skillosi_id
    SKILLOSI_DICT[skillosi_id] = item_dict
    
    for i, entry in enumerate(SKILLOSI_DATA):
        if entry["id"] == skillosi_id:
            SKILLOSI_DATA[i] = item_dict
            break
    
    return item_dict

@app.delete("/skillosi/{skillosi_id}")
def delete(skillosi_id: int):
    if skillosi_id not in SKILLOSI_DICT:
        return {"error": "id not found."}
    
    SKILLOSI_DICT.pop(skillosi_id)
    SKILLOSI_DATA[:] = [item for item in SKILLOSI_DATA if item["id"] != skillosi_id]
    
    return {"deleted": skillosi_id}
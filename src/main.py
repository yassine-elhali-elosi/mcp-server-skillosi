from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("skillosi")

SKILLOSI_API_BASE = "http://localhost:8000/skillosi"
USER_AGENT = "skillosi-app/1.0"

###

async def call_skillosi_api(url: str, method: str = "GET", data: Any = None) -> dict[str, Any] | None:
    """
    Make a request to the Skillosi API to manipulate employees data.
    Args:
        url (str): The API route URL to make the request to.
        method (str): The HTTP method to use (GET, POST, PUT).
        data (Any): The data to send with the request (for POST/PUT).
    Returns:
        dict[str, Any] | None: The JSON response from the API or None if an error occurs.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=data, headers=headers, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, json=data, headers=headers, timeout=30.0)
            else:
                return None
            
            response.raise_for_status()
            return response.json()
        
        except Exception:
            return None
        
def format_employee(employee: dict) -> str:
    """
    Format an employee data into a readable string.
    Args:
        employee (dict): The employee data.
    Returns:
        str: Formatted string of the employee data.
    """

    return f"""
        id: {employee.get('id', 'Unknown')}
        First name: {employee.get('firstName', 'Unknown')}
        Last name: {employee.get('lastName', 'Unknown')}
        Current work location: {employee.get('currentWorkLocation', 'Unknown')}
        Service: {employee.get('service', 'Unknown')}
    """

###

@mcp.tool()
async def get_all_employees() -> str:
    """
    Get all employees.
    Returns:
        str: Formatted string of all employees.
    """
    url = SKILLOSI_API_BASE
    data = await call_skillosi_api(url, method="GET")

    if not data:
        return "Unable to get all employees or no employees found."
    
    if not isinstance(data, list) or not data:
        return "No employees found."

    employees = [format_employee(employee) for employee in data]
    return "\n---\n".join(employees)

@mcp.tool()
async def get_employee_by_id(employee_id: int) -> str:
    """
    Get an employee by ID.
    Args:
        employee_id (int): The ID of the employee.
    Returns:
        str: Formatted string of the employee data.
    """
    url = f"{SKILLOSI_API_BASE}/{employee_id}"
    data = await call_skillosi_api(url, method="GET")

    if not data:
        return "Unable to get employee with id " + employee_id + "."
    
    return format_employee(data)

@mcp.tool()
async def create_employee(employee: dict) -> str:
    """
    Create a new employee.
    Args:
        employee (dict): The employee data to create.
    """
    url = SKILLOSI_API_BASE
    data = await call_skillosi_api(url, method="POST", data=employee)

    if not data:    
        return "Unable to create an employee."
    
    return format_employee(data)

### mcp.tool() for update
# ...

### mcp.tool() for delete
# ...

if __name__ == "__main__":
    mcp.run(transport="stdio")
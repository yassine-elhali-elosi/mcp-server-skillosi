from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import mantis_scrapping

mcp = FastMCP("elosi")

SKILLOSI_API_BASE = "http://localhost:8000/elosi"
USER_AGENT = "elosi-app/1.0"

###

async def make_elosi_request(url: str, method: str = "GET", data: Any = None) -> dict[str, Any] | None:
    """
    Make a request to the Skillosi API to manipulate employee data.
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
        
def format_skillosi(item: dict) -> str:
    """
    Format a Skillosi employee data into a readable string.
    Args:
        item (dict): The Skillosi employee data.
    Returns:
        str: Formatted string of the Skillosi employee data.
    """

    return f"""
        id: {item.get('id', 'Unknown')}
        First name: {item.get('firstName', 'Unknown')}
        Last name: {item.get('lastName', 'Unknown')}
        Current work location: {item.get('currentWorkLocation', 'Unknown')}
        Service: {item.get('service', 'Unknown')}
    """

###

@mcp.tool()
async def get_skillosi_all() -> str:
    """
    Fetch all Skillosi employees.
    Returns:
        str: Formatted string of all Skillosi employees.
    """
    url = SKILLOSI_API_BASE
    data = await make_elosi_request(url, method="GET")

    if not data:
        return "Unable to fetch Skillosi data or no data found."
    
    if not isinstance(data, list) or not data:
        return "No Skillosi entries found."

    skillosi_entries = [format_skillosi(item) for item in data]
    return "\n---\n".join(skillosi_entries)

@mcp.tool()
async def get_skillosi_by_id(skillosi_id: int) -> str:
    """
    Fetch a Skillosi employee by ID.
    Args:
        skillosi_id (int): The ID of the Skillosi employee.
    Returns:
        str: Formatted string of the Skillosi employee data.
    """
    url = f"{SKILLOSI_API_BASE}/{skillosi_id}"
    data = await make_elosi_request(url, method="GET")

    if not data:
        return "Unable to fetch Skillosi data or no data found."
    
    return format_skillosi(data)

@mcp.tool()
async def create_skillosi(item: dict) -> str:
    """
    Create a new Skillosi employee.
    Args:
        item (dict): The Skillosi employee data to create.
    """
    url = SKILLOSI_API_BASE
    data = await make_elosi_request(url, method="POST", data=item)

    if not data:    
        return "Unable to create Skillosi entry."
    
    return format_skillosi(data)

@mcp.tool()
async def get_mantis_tasks() -> str:
    """
    Fetch tasks/activities from Mantis.
    Returns:
        str: Formatted string of Mantis tasks.
    """
    bugnotes = mantis_scrapping.scrape_project()
    
    if not bugnotes:
        return "No Mantis tasks found."
    
    return bugnotes

### mcp.tool() for update

if __name__ == "__main__":
    mcp.run(transport="stdio")
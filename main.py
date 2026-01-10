import os
from dotenv import load_dotenv

# Load environment variables before importing modules that depend on them
load_dotenv()

from mcp.server.fastmcp import FastMCP
from modules import fhir

# Initialize FastMCP
port = int(os.environ.get("PORT", 8000))

mcp = FastMCP(
    "HAPI-FHIR-Server", 
    host="0.0.0.0", 
    port=port
)

# --- Generic FHIR Tools ---

@mcp.tool()
def create_resource(resource_type: str, resource: dict) -> dict:
    """
    Create a new FHIR resource.
    
    Args:
        resource_type: The type of resource (e.g., "Patient", "Observation").
        resource: The resource data.
    """
    return fhir.create_resource(resource_type, resource)

@mcp.tool()
def read_resource(resource_type: str, resource_id: str) -> dict:
    """
    Read a FHIR resource by ID.
    
    Args:
        resource_type: The type of resource.
        resource_id: The ID of the resource.
    """
    return fhir.read_resource(resource_type, resource_id)

@mcp.tool()
def update_resource(resource_type: str, resource_id: str, resource: dict) -> dict:
    """
    Update a FHIR resource.
    
    Args:
        resource_type: The type of resource.
        resource_id: The ID of the resource.
        resource: The updated resource data.
    """
    return fhir.update_resource(resource_type, resource_id, resource)

@mcp.tool()
def delete_resource(resource_type: str, resource_id: str) -> str:
    """
    Delete a FHIR resource.
    
    Args:
        resource_type: The type of resource.
        resource_id: The ID of the resource.
    """
    return fhir.delete_resource(resource_type, resource_id)

@mcp.tool()
def search_resources(resource_type: str, query: str = None) -> dict:
    """
    Search for FHIR resources.
    
    Args:
        resource_type: The type of resource.
        query: The query string (e.g., "name=doe&active=true").
    """
    return fhir.search_resources(resource_type, query)

@mcp.tool()
def create_transaction(bundle: dict) -> dict:
    """
    Process a FHIR transaction bundle.
    
    Args:
        bundle: The FHIR Bundle resource.
    """
    return fhir.create_transaction(bundle)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")


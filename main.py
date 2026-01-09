from mcp.server.fastmcp import FastMCP
from modules import patient
import os

# Initialize FastMCP
port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("HAPI-FHIR-Server", host="0.0.0.0", port=port)

# Register Patient Tools
@mcp.tool()
def create_patient(patient_resource: dict, auth_token: str) -> dict:
    """
    Create a new Patient resource (FHIR v4).
    
    Endpoint: POST [base]/Patient
    Creates a new patient resource with a server-assigned ID.
    
    Args:
        patient_resource: Dictionary containing FHIR Patient resource data.
        auth_token: JWT Bearer token.
    """
    return patient.create_patient(patient_resource, auth_token)

@mcp.tool()
def get_patient(patient_id: str, auth_token: str) -> dict:
    """
    Retrieve a Patient resource by ID (FHIR v4).
    
    Endpoint: GET [base]/Patient/[id]
    Retrieves the complete patient record.
    
    Args:
        patient_id: The unique FHIR ID of the patient.
        auth_token: JWT Bearer token.
    """
    return patient.get_patient(patient_id, auth_token)

@mcp.tool()
def update_patient(patient_id: str, patient_resource: dict, auth_token: str) -> dict:
    """
    Update an existing Patient resource (FHIR v4).
    
    Endpoint: PUT [base]/Patient/[id]
    Updates an existing resource or creates it if allowed.
    
    Args:
        patient_id: The unique FHIR ID of the patient.
        patient_resource: Updated FHIR Patient resource data.
        auth_token: JWT Bearer token.
    """
    return patient.update_patient(patient_id, patient_resource, auth_token)

@mcp.tool()
def delete_patient(patient_id: str, auth_token: str) -> str:
    """
    Delete a Patient resource by ID (FHIR v4).
    
    Endpoint: DELETE [base]/Patient/[id]
    
    Args:
        patient_id: The unique FHIR ID of the patient.
        auth_token: JWT Bearer token.
    """
    return patient.delete_patient(patient_id, auth_token)

@mcp.tool()
def search_patient(
    auth_token: str, 
    name: str = None, 
    identifier: str = None,
    family: str = None,
    given: str = None,
    gender: str = None,
    birthdate: str = None,
    address: str = None,
    email: str = None,
    phone: str = None,
    organization: str = None,
    active: bool = None
) -> dict:
    """
    Search for Patients using FHIR v4 parameters.
    
    Available Filters:
    - name: Matches any name part
    - family: Family name
    - given: Given name
    - gender: male | female | other | unknown
    - birthdate: YYYY-MM-DD
    - identifier: MRN, SSN, etc.
    - address: Address component
    - email: Email address
    - phone: Phone number
    - organization: Managing organization
    - active: Active status (True/False)
    """
    return patient.search_patient(
        auth_token, name, identifier, family, given, gender, 
        birthdate, address, email, phone, organization, active
    )
    
if __name__ == "__main__":
    mcp.run(transport="streamable-http")


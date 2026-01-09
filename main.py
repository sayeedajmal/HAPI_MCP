import os
from dotenv import load_dotenv

# Load environment variables before importing modules that depend on them
load_dotenv()

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.auth.settings import AuthSettings
from modules import patient
from modules.auth_verifier import FHIRTokenVerifier

# Initialize FastMCP with Authentication
port = int(os.environ.get("PORT", 8000))

# Configure Auth Settings
fhir_base_url = os.getenv("FHIR_BASE_URL", "http://172.20.10.14:8080/fhir")
# Derive issuer and resource server from base URL if possible
# For HAPI FHIR, usually the base is the resource server.
auth_settings = AuthSettings(
    issuer_url=fhir_base_url.replace("/fhir", ""), 
    resource_server_url=fhir_base_url
)

mcp = FastMCP(
    "HAPI-FHIR-Server", 
    host="0.0.0.0", 
    port=port,
    auth=auth_settings,
    token_verifier=FHIRTokenVerifier()
)

# Register Patient Tools
@mcp.tool()
def create_patient(patient_resource: dict, ctx: Context) -> dict:
    """
    Create a new Patient resource (FHIR v4).
    
    Endpoint: POST [base]/Patient
    Creates a new patient resource with a server-assigned ID.
    
    Args:
        patient_resource: Dictionary containing FHIR Patient resource data.
    """
    token = ctx.request_context.request.user.access_token.token
    return patient.create_patient(patient_resource, token)

@mcp.tool()
def get_patient(patient_id: str, ctx: Context) -> dict:
    """
    Retrieve a Patient resource by ID (FHIR v4).
    
    Endpoint: GET [base]/Patient/[id]
    Retrieves the complete patient record.
    
    Args:
        patient_id: The unique FHIR ID of the patient.
    """
    token = ctx.request_context.request.user.access_token.token
    return patient.get_patient(patient_id, token)

@mcp.tool()
def update_patient(patient_id: str, patient_resource: dict, ctx: Context) -> dict:
    """
    Update an existing Patient resource (FHIR v4).
    
    Endpoint: PUT [base]/Patient/[id]
    Updates an existing resource or creates it if allowed.
    
    Args:
        patient_id: The unique FHIR ID of the patient.
        patient_resource: Updated FHIR Patient resource data.
    """
    token = ctx.request_context.request.user.access_token.token
    return patient.update_patient(patient_id, patient_resource, token)

@mcp.tool()
def delete_patient(patient_id: str, ctx: Context) -> str:
    """
    Delete a Patient resource by ID (FHIR v4).
    
    Endpoint: DELETE [base]/Patient/[id]
    
    Args:
        patient_id: The unique FHIR ID of the patient.
    """
    token = ctx.request_context.request.user.access_token.token
    return patient.delete_patient(patient_id, token)

@mcp.tool()
def search_patient(
    ctx: Context,
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
    token = ctx.request_context.request.user.access_token.token
    return patient.search_patient(
        token, name, identifier, family, given, gender, 
        birthdate, address, email, phone, organization, active
    )
    
if __name__ == "__main__":
    mcp.run(transport="streamable-http")


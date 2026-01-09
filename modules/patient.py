"""
FHIR v4 Patient Resource Module.

The Patient resource covers demographic and administrative information about an individual 
receiving care or other health-related services.

Core Attributes:
- identifier: Patient identifiers (e.g., MRN, SSN)
- active: Whether the record is in active use
- name: Human names (family, given, prefix, suffix)
- telecom: Contact points (phone, email, fax)
- gender: Administrative gender (male | female | other | unknown)
- birthDate: Date of birth
- deceased[x]: Death indicator (boolean or dateTime)
- address: Physical addresses
- contact: Emergency contacts/guardians
- communication: Languages spoken
- generalPractitioner: Primary care provider references
- managingOrganization: Organization managing the record
"""

from typing import Dict, Optional, Any
import requests
import os

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "https://fhir.datainterops.com/fhir")

def get_headers(auth_token: str) -> Dict[str, str]:
    """
    Get headers for FHIR requests using the provided JWT token.
    
    Args:
        auth_token: The Bearer token for authentication.
    Returns:
        A dictionary containing the Authorization and Content-Type headers.
    """
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json",
    }

def create_patient(patient_resource: Dict[str, Any], auth_token: str) -> Dict[str, Any]:
    """
    Create a new Patient resource.
    
    Endpoint: POST [base]/Patient
    
    Creates a new patient resource with a server-assigned ID. 
    Can also be used with PUT [base]/Patient/[id] for client-assigned IDs.
    
    Args:
        patient_resource: The Patient resource data to create.
        auth_token: Authentication token.
    """
    url = f"{FHIR_BASE_URL}/Patient"
    response = requests.post(url, json=patient_resource, headers=get_headers(auth_token))
    response.raise_for_status()
    return response.json()

def get_patient(patient_id: str, auth_token: str) -> Dict[str, Any]:
    """
    Retrieve a Patient resource by ID.
    
    Endpoint: GET [base]/Patient/[id]
    
    Retrieves the complete patient record with all data elements.
    
    Args:
        patient_id: The unique ID of the patient.
        auth_token: Authentication token.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.get(url, headers=get_headers(auth_token))
    response.raise_for_status()
    return response.json()

def update_patient(patient_id: str, patient_resource: Dict[str, Any], auth_token: str) -> Dict[str, Any]:
    """
    Update an existing Patient resource.
    
    Endpoint: PUT [base]/Patient/[id]
    
    Updates an existing patient resource or creates it if it doesn't exist 
    (if the server is configured to allow client-assigned IDs).
    
    Args:
        patient_id: The unique ID of the patient to update.
        patient_resource: The updated Patient resource data.
        auth_token: Authentication token.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    patient_resource["id"] = patient_id
    response = requests.put(url, json=patient_resource, headers=get_headers(auth_token))
    response.raise_for_status()
    return response.json()

def delete_patient(patient_id: str, auth_token: str) -> str:
    """
    Delete a Patient resource by ID.
    
    Endpoint: DELETE [base]/Patient/[id]
    
    Removes a patient resource from the system.
    
    Args:
        patient_id: The unique ID of the patient to delete.
        auth_token: Authentication token.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.delete(url, headers=get_headers(auth_token))
    response.raise_for_status()
    return f"Patient {patient_id} deleted successfully."

def search_patient(
    auth_token: str, 
    name: Optional[str] = None, 
    identifier: Optional[str] = None,
    family: Optional[str] = None,
    given: Optional[str] = None,
    gender: Optional[str] = None,
    birthdate: Optional[str] = None,
    address: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    organization: Optional[str] = None,
    active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search for Patients using various FHIR v4 search parameters.
    
    Endpoint: GET [base]/Patient?[params]
    
    Common Search Parameters:
    - name: Matches any part of the name (family, given, etc.)
    - family: Search by family name
    - given: Search by given name
    - gender: male | female | other | unknown
    - birthdate: Date of birth (YYYY-MM-DD)
    - identifier: MRN, SSN, etc.
    - address: Any address component
    - email: Search by email address
    - phone: Search by phone number
    - organization: Filter by managing organization
    - active: Filter by active status (true/false)
    
    Args:
        auth_token: Authentication token.
        **kwargs: Various search filters.
    """
    params = {}
    if name: params["name"] = name
    if family: params["family"] = family
    if given: params["given"] = given
    if gender: params["gender"] = gender
    if birthdate: params["birthdate"] = birthdate
    if identifier: params["identifier"] = identifier
    if address: params["address"] = address
    if email: params["email"] = email
    if phone: params["phone"] = phone
    if organization: params["organization"] = organization
    if active is not None: params["active"] = str(active).lower()
    
    url = f"{FHIR_BASE_URL}/Patient"
    response = requests.get(url, params=params, headers=get_headers(auth_token))
    response.raise_for_status()
    return response.json()


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

from typing import Dict, Optional, Any, Union
import requests
import os

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL")
if not FHIR_BASE_URL:
    raise ValueError("FHIR_BASE_URL environment variable is not set")

def get_headers() -> Dict[str, str]:
    """
    Get headers for FHIR requests.
    
    Returns:
        A dictionary containing the Content-Type and Accept headers.
    """
    return {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json",
    }

def _handle_response(response: requests.Response) -> Union[Dict[str, Any], str]:
    """
    Handle the response from the FHIR server.
    If success, return JSON.
    If error, return the error JSON (OperationOutcome) or raise with details.
    """
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        # Try to return the OperationOutcome if available
        try:
            return response.json()
        except ValueError:
            # If not JSON, raise the original error with text
            raise ValueError(f"FHIR Server Error ({response.status_code}): {response.text}")

def create_patient(patient_resource: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Create a new Patient resource.
    
    Endpoint: POST [base]/Patient
    
    Creates a new patient resource with a server-assigned ID. 
    Can also be used with PUT [base]/Patient/[id] for client-assigned IDs.
    
    Args:
        patient_resource: The Patient resource data to create.
    """
    url = f"{FHIR_BASE_URL}/Patient"
    response = requests.post(url, json=patient_resource, headers=get_headers())
    return _handle_response(response)

def get_patient(patient_id: str) -> Union[Dict[str, Any], str]:
    """
    Retrieve a Patient resource by ID.
    
    Endpoint: GET [base]/Patient/[id]
    
    Retrieves the complete patient record with all data elements.
    
    Args:
        patient_id: The unique ID of the patient.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.get(url, headers=get_headers())
    return _handle_response(response)

def update_patient(patient_id: str, patient_resource: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Update an existing Patient resource.
    
    Endpoint: PUT [base]/Patient/[id]
    
    Updates an existing patient resource or creates it if it doesn't exist 
    (if the server is configured to allow client-assigned IDs).
    
    Args:
        patient_id: The unique ID of the patient to update.
        patient_resource: The updated Patient resource data.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    patient_resource["id"] = patient_id
    response = requests.put(url, json=patient_resource, headers=get_headers())
    return _handle_response(response)

def delete_patient(patient_id: str) -> str:
    """
    Delete a Patient resource by ID.
    
    Endpoint: DELETE [base]/Patient/[id]
    
    Removes a patient resource from the system.
    
    Args:
        patient_id: The unique ID of the patient to delete.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    response = requests.delete(url, headers=get_headers())
    try:
        response.raise_for_status()
        return f"Patient {patient_id} deleted successfully."
    except requests.exceptions.HTTPError:
        try:
            # Return OperationOutcome as string representation if possible, or just the error
            return str(response.json())
        except ValueError:
            raise ValueError(f"FHIR Server Error ({response.status_code}): {response.text}")

def search_patient(
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
) -> Union[Dict[str, Any], str]:
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
    response = requests.get(url, params=params, headers=get_headers())
    return _handle_response(response)


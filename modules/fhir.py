"""
Generic FHIR Resource Module.

This module provides generic functions to interact with any FHIR resource type.
It ports the logic from the Java McpFhirBridge and RequestBuilder classes.
"""

from typing import Dict, Optional, Any, Union, List
import requests
import os
import json

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL")
if not FHIR_BASE_URL:
    raise ValueError("FHIR_BASE_URL environment variable is not set")

def get_headers() -> Dict[str, str]:
    """
    Get headers for FHIR requests.
    """
    return {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json",
    }

def _handle_response(response: requests.Response) -> Union[Dict[str, Any], str]:
    """
    Handle the response from the FHIR server.
    """
    try:
        response.raise_for_status()
        if response.status_code == 204:
            return "Success (No Content)"
        return response.json()
    except requests.exceptions.HTTPError:
        try:
            return response.json()
        except ValueError:
            raise ValueError(f"FHIR Server Error ({response.status_code}): {response.text}")

def create_resource(resource_type: str, resource: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Create a new FHIR resource.
    
    Args:
        resource_type: The type of resource to create (e.g., "Patient", "Observation").
        resource: The resource data.
    """
    url = f"{FHIR_BASE_URL}/{resource_type}"
    response = requests.post(url, json=resource, headers=get_headers())
    return _handle_response(response)

def read_resource(resource_type: str, resource_id: str) -> Union[Dict[str, Any], str]:
    """
    Read a FHIR resource by ID.
    
    Args:
        resource_type: The type of resource to read.
        resource_id: The ID of the resource.
    """
    url = f"{FHIR_BASE_URL}/{resource_type}/{resource_id}"
    response = requests.get(url, headers=get_headers())
    return _handle_response(response)

def update_resource(resource_type: str, resource_id: str, resource: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Update a FHIR resource.
    
    Args:
        resource_type: The type of resource to update.
        resource_id: The ID of the resource.
        resource: The updated resource data.
    """
    url = f"{FHIR_BASE_URL}/{resource_type}/{resource_id}"
    # Ensure ID is in the resource body
    if "id" not in resource:
        resource["id"] = resource_id
        
    response = requests.put(url, json=resource, headers=get_headers())
    return _handle_response(response)

def delete_resource(resource_type: str, resource_id: str) -> str:
    """
    Delete a FHIR resource.
    
    Args:
        resource_type: The type of resource to delete.
        resource_id: The ID of the resource.
    """
    url = f"{FHIR_BASE_URL}/{resource_type}/{resource_id}"
    response = requests.delete(url, headers=get_headers())
    try:
        response.raise_for_status()
        return f"{resource_type} {resource_id} deleted successfully."
    except requests.exceptions.HTTPError:
        try:
            return str(response.json())
        except ValueError:
            raise ValueError(f"FHIR Server Error ({response.status_code}): {response.text}")

def patch_resource(resource_type: str, resource_id: str, patch_body: Any) -> Union[Dict[str, Any], str]:
    """
    Patch a FHIR resource.
    
    Args:
        resource_type: The type of resource to patch.
        resource_id: The ID of the resource.
        patch_body: The patch content (JSON Patch or FHIR Patch).
    """
    url = f"{FHIR_BASE_URL}/{resource_type}/{resource_id}"
    
    # Determine Content-Type based on patch body structure if needed, 
    # but for now we stick to fhir+json or json-patch+json
    headers = get_headers()
    headers["Content-Type"] = "application/json-patch+json" # Common for patches
    
    response = requests.patch(url, json=patch_body, headers=headers)
    return _handle_response(response)

def search_resources(resource_type: str, query: Optional[str] = None) -> Union[Dict[str, Any], str]:
    """
    Search for FHIR resources.
    
    Args:
        resource_type: The type of resource to search.
        query: The query string (e.g., "name=doe&active=true").
    """
    url = f"{FHIR_BASE_URL}/{resource_type}"
    params = {}
    if query:
        # Simple parsing of query string to dict for requests
        # Note: This handles basic key=value. Repeated keys might need special handling.
        for pair in query.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
                
    response = requests.get(url, params=params, headers=get_headers())
    return _handle_response(response)

def create_transaction(bundle: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Process a FHIR transaction bundle.
    
    Args:
        bundle: The FHIR Bundle resource.
    """
    url = f"{FHIR_BASE_URL}"
    response = requests.post(url, json=bundle, headers=get_headers())
    return _handle_response(response)

# Patient MCP Module Documentation

The Patient MCP module provides tools for performing CRUD (Create, Read, Update, Delete) and Search operations on Patient resources in a HAPI FHIR JPA server.

## Features

- **Passthrough Authentication**: Each operation requires a JWT `auth_token` provided by the client. This token is passed directly in the `Authorization` header to the FHIR server.
- **Resource Management**: Complete lifecycle management for Patient resources.
- **Search Capabilities**: Flexible searching by name or identifier.

## Tools and Parameters

### `create_patient`
Creates a new Patient resource.
- `patient_resource` (dict): A valid FHIR Patient JSON object.
- `auth_token` (str): JWT Bearer token for authentication.

### `get_patient`
Retrieves a specific Patient by their ID.
- `patient_id` (str): The unique identifier of the Patient on the FHIR server.
- `auth_token` (str): JWT Bearer token for authentication.

### `update_patient`
Updates an existing Patient resource.
- `patient_id` (str): The unique identifier of the Patient to update.
- `patient_resource` (dict): The updated Patient JSON object.
- `auth_token` (str): JWT Bearer token for authentication.

### `delete_patient`
Deletes a Patient resource.
- `patient_id` (str): The unique identifier of the Patient to delete.
- `auth_token` (str): JWT Bearer token for authentication.

### `search_patient`
Searches for patients based on criteria.
- `auth_token` (str): JWT Bearer token for authentication.
- `name` (str, optional): Search by name (given or family).
- `identifier` (str, optional): Search by identifier (e.g., SSN).

## Implementation Details

- **Module Path**: `modules/patient.py`
- **Dependency**: Uses the `requests` library for synchronous HTTP calls.
- **Base URL**: Configurable via `FHIR_BASE_URL` in the `.env` file (defaults to `https://fhir.datainterops.com/fhir`).

## Error Handling

The tools use `response.raise_for_status()`, which will raise an exception if the FHIR server returns a 4xx or 5xx error. These errors are then bubbled up to the MCP client (e.g., Claude or ChatGPT).

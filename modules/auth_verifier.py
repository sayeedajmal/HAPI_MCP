from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.fastmcp import Context
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class FHIRTokenVerifier(TokenVerifier):
    def __init__(self):
        base_url = os.getenv("FHIR_BASE_URL", "http://172.20.10.14:8080/fhir")
        # Normalize URL: remove trailing slash
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        # Remove /fhir suffix if present to get the root
        if base_url.endswith('/fhir'):
            base_url = base_url[:-5]
            
        self._verification_url = f"{base_url}/isactive"

    async def verify_token(self, token: str) -> AccessToken | None:
        """
        Verify the token against the FHIR server.
        Returns an AccessToken if valid, None otherwise.
        """
        try:
            # We use a synchronous request here, but in a real async app 
            # we might want to use aiohttp or run in a thread executor.
            # For simplicity and since requests is already used, we'll use it.
            response = requests.get(
                self._verification_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                # Token is valid. We return an AccessToken object.
                # We can use the token itself as the client_id if no specific ID is returned,
                # or generate one. For now, we'll use a placeholder or hash of the token.
                return AccessToken(
                    token=token,
                    client_id="fhir_user", # In a real scenario, we might extract user ID from response
                    scopes=["fhir:read", "fhir:write"] # Default scopes
                )
            return None
        except Exception:
            return None

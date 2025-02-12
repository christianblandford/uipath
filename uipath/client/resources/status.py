from typing import Optional, Dict
from ..base_client import BaseClient

class StatusClient:
    """Client for checking UiPath service status"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def get(self) -> None:
        """
        Returns whether the current endpoint should be serving traffic.
        """
        return self._client._make_request('GET', '/api/Status/Get')

    def verify_host_availability(self, url: str) -> Dict:
        """
        Verify if a host is available.
        
        Args:
            url: The URL to verify
            
        Returns:
            Host availability status
        """
        params = {"url": url}
        return self._client._make_request(
            'GET',
            '/api/Status/VerifyHostAvailibility',
            params=params
        ) 
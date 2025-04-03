from typing import Dict
from ..base_client import BaseClient

class LicensingClient:
    """Client for managing UiPath licensing"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def acquire(self, license_data: Dict) -> Dict:
        """
        Acquire license units.
        
        Args:
            license_data: License consumption data
            
        Returns:
            License result details
        """
        return self._client._make_request(
            'POST',
            '/api/Licensing/Acquire',
            json=license_data
        )

    def release(self, license_data: Dict) -> Dict:
        """
        Release acquired license units.
        
        Args:
            license_data: License consumption data to release
            
        Returns:
            License result details
        """
        return self._client._make_request(
            'PUT',
            '/api/Licensing/Release',
            json=license_data
        ) 
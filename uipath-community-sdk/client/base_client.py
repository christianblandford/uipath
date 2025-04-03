import requests
from typing import Optional, Dict, Any, BinaryIO
from ..auth.authentication import UiPathAuth

class BaseClient:
    def __init__(
        self,
        auth: UiPathAuth,
        base_url: str
    ):
        self.auth = auth
        self.base_url = base_url.rstrip('/')

    def _make_request(
        self, 
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        files: Optional[Dict] = None,
        raw_response: bool = False
    ) -> Any:
        """Make HTTP request to UiPath API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.auth.get_headers()
        
        # Remove content-type header if uploading files
        if files:
            headers.pop('Content-Type', None)
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
            files=files
        )
        response.raise_for_status()
        
        if raw_response:
            return response
            
        if response.content:
            return response.json()
        return None 
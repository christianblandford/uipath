import requests
from typing import Optional, Dict

class UiPathAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scope: str = "OR.Assets",
        tenant_name: Optional[str] = None,
        organization_id: Optional[str] = None,
        auth_url: str = "https://cloud.uipath.com/identity_/connect/token"
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.tenant_name = tenant_name
        self.organization_id = organization_id
        self.auth_url = auth_url
        self._token = None

    def get_token(self) -> str:
        """Get OAuth token, refreshing if necessary"""
        if not self._token:
            self._token = self._fetch_token()
        return self._token

    def _fetch_token(self) -> str:
        """Fetch new OAuth token"""
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }

        response = requests.post(self.auth_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        return token_data['access_token']

    def get_headers(self) -> Dict[str, str]:
        """Get headers needed for API requests"""
        headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }
        
        if self.organization_id:
            headers['X-UIPATH-OrganizationUnitId'] = self.organization_id
            
        return headers 
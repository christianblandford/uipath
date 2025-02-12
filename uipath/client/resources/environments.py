from typing import Optional, Dict, List
from ..base_client import BaseClient

class EnvironmentsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(
        self,
        name: Optional[str] = None,
        organization_unit_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Get environments with optional filters.
        
        Args:
            name: Filter by environment name
            organization_unit_id: Filter by organization unit ID
        """
        filters = []
        if name:
            filters.append(f"Name eq '{name}'")
        if organization_unit_id:
            filters.append(f"OrganizationUnitId eq {organization_unit_id}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/Environments', params=params)

    def get_by_id(self, environment_id: int) -> Dict:
        """Get environment by ID"""
        return self._client._make_request('GET', f'/odata/Environments({environment_id})')

    def create(self, environment_data: Dict) -> Dict:
        """
        Create a new environment.
        
        Args:
            environment_data: Dict containing environment details including:
                - Name: Environment name
                - Description: Optional description
                - Type: Environment type
                - OrganizationUnitId: Optional organization unit ID
        """
        return self._client._make_request('POST', '/odata/Environments', json=environment_data)

    def update(self, environment_id: int, environment_data: Dict) -> Dict:
        """
        Update an existing environment.
        
        Args:
            environment_id: ID of environment to update
            environment_data: Updated environment data
        """
        return self._client._make_request(
            'PUT',
            f'/odata/Environments({environment_id})',
            json=environment_data
        )

    def delete(self, environment_id: int) -> None:
        """Delete an environment"""
        self._client._make_request('DELETE', f'/odata/Environments({environment_id})') 
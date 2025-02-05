from typing import Optional, Dict, List
from ..base_client import BaseClient

class AssetsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(self, name: Optional[str] = None) -> List[Dict]:
        """
        Get assets. If name is provided, filter by name.
        """
        params = {"$filter": f"Name eq '{name}'"} if name else None
        return self._client._make_request('GET', '/odata/Assets', params=params)

    def get_by_id(self, asset_id: int) -> Dict:
        """Get asset by ID"""
        return self._client._make_request('GET', f'/odata/Assets({asset_id})')

    def create(self, asset_data: Dict) -> Dict:
        """Create new asset"""
        return self._client._make_request('POST', '/odata/Assets', json=asset_data)

    def update(self, asset_id: int, asset_data: Dict) -> Dict:
        """Update existing asset"""
        return self._client._make_request('PUT', f'/odata/Assets({asset_id})', json=asset_data)

    def delete(self, asset_id: int) -> None:
        """Delete asset"""
        self._client._make_request('DELETE', f'/odata/Assets({asset_id})') 
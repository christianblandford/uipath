from typing import Optional, Dict, List, BinaryIO
from ..base_client import BaseClient

class PackagesClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        is_active: Optional[bool] = None,
        is_latest: Optional[bool] = None,
        package_key: Optional[str] = None
    ) -> List[Dict]:
        """
        Get packages with optional filters.
        
        Args:
            is_active: Filter by active status
            is_latest: Filter for latest versions only
            package_key: Filter by package key
        """
        filters = []
        if is_active is not None:
            filters.append(f"IsActive eq {str(is_active).lower()}")
        if is_latest is not None:
            filters.append(f"IsLatestVersion eq {str(is_latest).lower()}")
        if package_key:
            filters.append(f"Key eq '{package_key}'")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Processes', params=params)

    def get_by_id(self, package_id: int) -> Dict:
        """Get package by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Processes({package_id})')

    def get_by_key(self, key: str) -> Dict:
        """Get package by key"""
        filters = [f"Key eq '{key}'"]
        params = {"$filter": " and ".join(filters)}
        results = self._orchestrator._make_request('GET', '/odata/Processes', params=params)
        return results[0] if results else None

    def upload(self, file_path: str, version: Optional[str] = None) -> Dict:
        """
        Upload a new package (.nupkg file)
        
        Args:
            file_path: Path to the .nupkg file
            version: Optional version string
        """
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/octet-stream')}
            params = {'version': version} if version else None
            
            return self._orchestrator._make_request(
                'POST',
                '/odata/Processes/UiPath.Server.Configuration.OData.Upload',
                files=files,
                params=params
            )

    def upload_stream(self, file_stream: BinaryIO, filename: str, version: Optional[str] = None) -> Dict:
        """
        Upload a package from a file stream
        
        Args:
            file_stream: File-like object containing the package
            filename: Name of the file
            version: Optional version string
        """
        files = {'file': (filename, file_stream, 'application/octet-stream')}
        params = {'version': version} if version else None
        
        return self._orchestrator._make_request(
            'POST',
            '/odata/Processes/UiPath.Server.Configuration.OData.Upload',
            files=files,
            params=params
        )

    def download(self, package_id: int) -> bytes:
        """
        Download a package by ID
        
        Returns:
            bytes: The package content
        """
        response = self._orchestrator._make_request(
            'GET',
            f'/odata/Processes/UiPath.Server.Configuration.OData.Download({package_id})',
            raw_response=True
        )
        return response.content

    def delete(self, package_id: int) -> None:
        """Delete a package"""
        return self._orchestrator._make_request('DELETE', f'/odata/Processes({package_id})')

    def set_active(self, package_id: int, is_active: bool) -> None:
        """
        Set the active status of a package
        
        Args:
            package_id: ID of the package
            is_active: Whether the package should be active
        """
        data = {"isActive": is_active}
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Processes({package_id})/UiPath.Server.Configuration.OData.SetActive'
        ) 
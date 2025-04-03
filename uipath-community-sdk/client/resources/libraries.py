from typing import Optional, Dict, List, BinaryIO
from ..base_client import BaseClient

class LibrariesClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        version: Optional[str] = None,
        title: Optional[str] = None,
        is_latest: Optional[bool] = None
    ) -> List[Dict]:
        """
        Get libraries with optional filters.
        
        Args:
            version: Filter by version
            title: Filter by package title
            is_latest: Filter for latest versions only
        """
        filters = []
        if version:
            filters.append(f"Version eq '{version}'")
        if title:
            filters.append(f"Title eq '{title}'")
        if is_latest is not None:
            filters.append(f"IsLatestVersion eq {str(is_latest).lower()}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Libraries', params=params)

    def get_by_id(self, library_id: int) -> Dict:
        """Get library by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Libraries({library_id})')

    def upload(self, file_path: str) -> Dict:
        """
        Upload a new library package (.nupkg file)
        
        Args:
            file_path: Path to the .nupkg file
        """
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/octet-stream')}
            return self._orchestrator._make_request(
                'POST',
                '/odata/Libraries/UiPath.Server.Configuration.OData.Upload',
                files=files
            )

    def upload_stream(self, file_stream: BinaryIO, filename: str) -> Dict:
        """
        Upload a library from a file stream
        
        Args:
            file_stream: File-like object containing the library package
            filename: Name of the file
        """
        files = {'file': (filename, file_stream, 'application/octet-stream')}
        return self._orchestrator._make_request(
            'POST',
            '/odata/Libraries/UiPath.Server.Configuration.OData.Upload',
            files=files
        )

    def delete(self, library_id: int) -> None:
        """Delete a library"""
        return self._orchestrator._make_request('DELETE', f'/odata/Libraries({library_id})')

    def delete_version(self, library_id: int, version: str) -> None:
        """
        Delete a specific version of a library
        
        Args:
            library_id: ID of the library
            version: Version string to delete
        """
        return self._orchestrator._make_request(
            'DELETE',
            f'/odata/Libraries({library_id})/UiPath.Server.Configuration.OData.DeleteVersion',
            params={"version": version}
        )

    def get_versions(self, title: str) -> List[Dict]:
        """
        Get all versions of a specific library
        
        Args:
            title: The library title to get versions for
        """
        filters = [f"Title eq '{title}'"]
        params = {"$filter": " and ".join(filters)}
        return self._orchestrator._make_request('GET', '/odata/Libraries', params=params)

    def download(self, library_id: int) -> bytes:
        """
        Download a library package by ID
        
        Returns:
            bytes: The library package content
        """
        response = self._orchestrator._make_request(
            'GET',
            f'/odata/Libraries/UiPath.Server.Configuration.OData.Download({library_id})',
            raw_response=True
        )
        return response.content

    def get_dependencies(self, library_id: int) -> List[Dict]:
        """
        Get dependencies for a specific library
        
        Args:
            library_id: ID of the library
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Libraries({library_id})/UiPath.Server.Configuration.OData.GetDependencies'
        ) 
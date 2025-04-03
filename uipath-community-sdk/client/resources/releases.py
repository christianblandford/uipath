from typing import Optional, Dict, List
from ..base_client import BaseClient

class ReleasesClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        process_key: Optional[str] = None,
        is_latest: Optional[bool] = None,
        environment_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Get releases with optional filters.
        
        Args:
            process_key: Filter by process key
            is_latest: Filter for latest versions only
            environment_id: Filter by environment ID
        """
        filters = []
        if process_key:
            filters.append(f"ProcessKey eq '{process_key}'")
        if is_latest is not None:
            filters.append(f"IsLatestVersion eq {str(is_latest).lower()}")
        if environment_id:
            filters.append(f"EnvironmentId eq {environment_id}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Releases', params=params)

    def get_by_id(self, release_id: int) -> Dict:
        """Get release by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Releases({release_id})')

    def get_by_key(self, key: str) -> Dict:
        """Get release by key"""
        return self._orchestrator._make_request('GET', f'/odata/Releases/UiPath.Server.Configuration.OData.GetByKey(key=\'{key}\')')

    def create(self, release_data: Dict) -> Dict:
        """
        Create a new release
        
        Args:
            release_data: Dict containing release details including:
                - Name: Release name
                - ProcessKey: Process identifier
                - ProcessVersion: Version string
                - Description: Optional description
                - EnvironmentId: Target environment ID
                - EntryPointId: Process entry point
        """
        return self._orchestrator._make_request('POST', '/odata/Releases', json=release_data)

    def update(self, release_id: int, release_data: Dict) -> Dict:
        """
        Update an existing release
        
        Args:
            release_id: ID of the release to update
            release_data: Updated release data
        """
        return self._orchestrator._make_request(
            'PUT',
            f'/odata/Releases({release_id})',
            json=release_data
        )

    def delete(self, release_id: int) -> None:
        """Delete a release by ID"""
        return self._orchestrator._make_request('DELETE', f'/odata/Releases({release_id})')

    def delete_by_key(self, key: str) -> None:
        """Delete a release by key"""
        return self._orchestrator._make_request(
            'DELETE',
            f'/odata/Releases/UiPath.Server.Configuration.OData.DeleteByKey(key=\'{key}\')'
        )

    def update_process_settings(self, release_id: int, settings: Dict) -> Dict:
        """
        Update process settings for a release
        
        Args:
            release_id: ID of the release
            settings: Dict containing process settings
        """
        return self._orchestrator._make_request(
            'PUT',
            f'/odata/Releases({release_id})/UiPath.Server.Configuration.OData.UpdateProcessSettings',
            json=settings
        )

    def get_latest_version(self, process_key: str, environment_id: Optional[int] = None) -> Dict:
        """
        Get the latest version of a release for a specific process
        
        Args:
            process_key: Process identifier
            environment_id: Optional environment ID filter
        """
        filters = [
            f"ProcessKey eq '{process_key}'",
            "IsLatestVersion eq true"
        ]
        if environment_id:
            filters.append(f"EnvironmentId eq {environment_id}")
            
        params = {"$filter": " and ".join(filters)}
        results = self._orchestrator._make_request('GET', '/odata/Releases', params=params)
        
        # Return first result if any exists
        return results[0] if results else None 
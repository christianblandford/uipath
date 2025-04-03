from typing import Optional, Dict, List
from ..base_client import BaseClient

class StatsClient:
    """Client for retrieving UiPath statistics"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def get_consumption_license_stats(
        self,
        tenant_id: Optional[int] = None,
        days: Optional[int] = None
    ) -> List[Dict]:
        """
        Gets the consumption licensing usage statistics.
        
        Args:
            tenant_id: Optional tenant ID to get stats for
            days: Number of reported license usage days
            
        Returns:
            List of consumption license statistics
        """
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id
        if days:
            params["days"] = days
            
        return self._client._make_request(
            'GET',
            '/api/Stats/GetConsumptionLicenseStats',
            params=params
        )

    def get_count_stats(self) -> List[Dict]:
        """
        Gets the total number of various entities registered in Orchestrator.
        
        Returns:
            List of entity counts (Processes, Assets, Queues, etc)
        """
        return self._client._make_request('GET', '/api/Stats/GetCountStats')

    def get_jobs_stats(self) -> List[Dict]:
        """
        Gets the total number of jobs aggregated by Job State.
        
        Returns:
            List of job counts by state (Successful, Faulted, Canceled)
        """
        return self._client._make_request('GET', '/api/Stats/GetJobsStats')

    def get_license_stats(
        self,
        tenant_id: Optional[int] = None,
        days: Optional[int] = None
    ) -> List[Dict]:
        """
        Gets the licensing usage statistics.
        
        Args:
            tenant_id: Optional tenant ID to get stats for
            days: Number of reported license usage days
            
        Returns:
            List of license statistics
        """
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id
        if days:
            params["days"] = days
            
        return self._client._make_request(
            'GET',
            '/api/Stats/GetLicenseStats',
            params=params
        )

    def get_sessions_stats(self) -> List[Dict]:
        """
        Gets the total number of robots aggregated by Robot State.
        
        Returns:
            List of robot counts by state (Available, Busy, Disconnected, Unresponsive)
        """
        return self._client._make_request('GET', '/api/Stats/GetSessionsStats') 
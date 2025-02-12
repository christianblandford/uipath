from typing import Optional, Dict, List
from ..base_client import BaseClient

class MaintenanceClient:
    """Client for managing UiPath maintenance operations"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def end(self, tenant_id: Optional[int] = None) -> None:
        """
        Ends a maintenance window.
        
        Args:
            tenant_id: Optional tenant ID to end maintenance for
        """
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id
            
        self._client._make_request('POST', '/api/Maintenance/End', params=params)

    def get(self, tenant_id: Optional[int] = None) -> Dict:
        """
        Gets the maintenance settings.
        
        Args:
            tenant_id: Optional tenant ID to get settings for
            
        Returns:
            Maintenance settings
        """
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id
            
        return self._client._make_request('GET', '/api/Maintenance/Get', params=params)

    def start(
        self,
        phase: str,
        force: bool = False,
        kill_jobs: bool = False,
        tenant_id: Optional[int] = None
    ) -> None:
        """
        Starts a maintenance window.
        
        Args:
            phase: Maintenance phase (Draining or Suspended)
            force: Whether to ignore errors during transition
            kill_jobs: Whether to force-kill running jobs when transitioning to Suspended
            tenant_id: Optional tenant ID to start maintenance for
        """
        params = {
            "phase": phase,
            "force": force,
            "killJobs": kill_jobs
        }
        if tenant_id:
            params["tenantId"] = tenant_id
            
        self._client._make_request('POST', '/api/Maintenance/Start', params=params)

    def get_status(self) -> Dict:
        """Get maintenance mode status"""
        return self._client._make_request('GET', '/api/Maintenance/Status')

    def enable(self, drain_time: Optional[int] = None) -> None:
        """
        Enable maintenance mode.
        
        Args:
            drain_time: Optional drain time in minutes
        """
        data = {"drainTimeMinutes": drain_time} if drain_time else {}
        self._client._make_request('POST', '/api/Maintenance/Enable', json=data)

    def disable(self) -> None:
        """Disable maintenance mode"""
        self._client._make_request('POST', '/api/Maintenance/Disable')

    def get_active_sessions(self) -> List[Dict]:
        """Get list of active sessions during maintenance"""
        return self._client._make_request('GET', '/api/Maintenance/ActiveSessions') 
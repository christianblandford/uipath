from typing import Optional, Dict, List
from ..base_client import BaseClient

class ProcessesClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        name: Optional[str] = None,
        is_latest: Optional[bool] = None,
        environment_id: Optional[int] = None,
        package_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Get processes with optional filters.
        
        Args:
            name: Filter by process name
            is_latest: Filter for latest versions only
            environment_id: Filter by environment ID
            package_id: Filter by package ID
        """
        filters = []
        if name:
            filters.append(f"Name eq '{name}'")
        if is_latest is not None:
            filters.append(f"IsLatestVersion eq {str(is_latest).lower()}")
        if environment_id:
            filters.append(f"EnvironmentId eq {environment_id}")
        if package_id:
            filters.append(f"PackageId eq {package_id}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Processes', params=params)

    def get_by_id(self, process_id: int) -> Dict:
        """Get process by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Processes({process_id})')

    def create(self, process_data: Dict) -> Dict:
        """
        Create a new process
        
        Args:
            process_data: Dict containing process details including:
                - Name: Process name
                - PackageId: Associated package ID
                - EnvironmentId: Target environment ID
                - Description: Optional description
        """
        return self._orchestrator._make_request('POST', '/odata/Processes', json=process_data)

    def update(self, process_id: int, process_data: Dict) -> Dict:
        """
        Update an existing process
        
        Args:
            process_id: ID of the process to update
            process_data: Updated process data
        """
        return self._orchestrator._make_request(
            'PUT',
            f'/odata/Processes({process_id})',
            json=process_data
        )

    def delete(self, process_id: int) -> None:
        """Delete a process"""
        return self._orchestrator._make_request('DELETE', f'/odata/Processes({process_id})')

    def get_versions(self, process_key: str) -> List[Dict]:
        """
        Get all versions of a specific process
        
        Args:
            process_key: The process key to get versions for
        """
        filters = [f"ProcessKey eq '{process_key}'"]
        params = {"$filter": " and ".join(filters)}
        return self._orchestrator._make_request('GET', '/odata/Processes', params=params)

    def get_process_schedule(self, process_id: int) -> Dict:
        """
        Get schedule information for a process
        
        Args:
            process_id: ID of the process
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.GetProcessSchedule'
        )

    def set_process_schedule(self, process_id: int, schedule_data: Dict) -> None:
        """
        Set schedule for a process
        
        Args:
            process_id: ID of the process
            schedule_data: Schedule configuration including:
                - Enabled: Whether schedule is enabled
                - CronExpression: Cron expression for scheduling
                - TimeZoneId: Timezone for scheduling
                - StartProcessCron: Start process cron details
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.SetProcessSchedule',
            json=schedule_data
        )

    def get_process_parameters(self, process_id: int) -> List[Dict]:
        """
        Get parameters for a process
        
        Args:
            process_id: ID of the process
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.GetProcessParameters'
        )

    def set_process_parameters(self, process_id: int, parameters: List[Dict]) -> None:
        """
        Set parameters for a process
        
        Args:
            process_id: ID of the process
            parameters: List of parameter configurations
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.SetProcessParameters',
            json=parameters
        )

    def start_process(
        self,
        process_id: int,
        robot_ids: Optional[List[int]] = None,
        input_arguments: Optional[Dict] = None
    ) -> Dict:
        """
        Start a process execution
        
        Args:
            process_id: ID of the process to start
            robot_ids: Optional list of robot IDs to run the process
            input_arguments: Optional input arguments for the process
        """
        data = {
            "robotIds": robot_ids or [],
            "inputArguments": input_arguments or {}
        }
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.StartProcess',
            json=data
        )

    def stop_process(self, process_id: int) -> None:
        """
        Stop a running process
        
        Args:
            process_id: ID of the process to stop
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Processes({process_id})/UiPath.Server.Configuration.OData.StopProcess'
        ) 
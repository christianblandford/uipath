from typing import Optional, Dict, List, Union
from ..base_client import BaseClient

class JobsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(
        self,
        state: Optional[str] = None,
        robot_name: Optional[str] = None,
        process_name: Optional[str] = None
    ) -> List[Dict]:
        """
        Get jobs with optional filters.
        
        Args:
            state: Filter by job state (Pending, Running, Stopping, Terminating, 
                  Faulted, Successful, Stopped, Suspended, Resumed)
            robot_name: Filter by robot name
            process_name: Filter by process name
        """
        filters = []
        if state:
            filters.append(f"State eq '{state}'")
        if robot_name:
            filters.append(f"Robot/Name eq '{robot_name}'")
        if process_name:
            filters.append(f"ReleaseName eq '{process_name}'")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/Jobs', params=params)

    def get_by_id(self, job_id: int) -> Dict:
        """Get job by ID"""
        return self._client._make_request('GET', f'/odata/Jobs({job_id})')

    def start_jobs(self, release_key: str, robot_ids: Optional[List[int]] = None, 
                  strategy: str = "Specific", input_arguments: Optional[Dict] = None) -> Dict:
        """
        Start new jobs for a specific release.
        
        Args:
            release_key: The unique key of the release to run
            robot_ids: List of robot IDs to run the jobs on (required if strategy is "Specific")
            strategy: Job allocation strategy ("All", "Specific", "RobotCount", "JobsCount")
            input_arguments: Input arguments for the jobs
        """
        data = {
            "startInfo": {
                "ReleaseKey": release_key,
                "Strategy": strategy,
                "RobotIds": robot_ids or [],
                "Source": "Manual",
                "InputArguments": input_arguments
            }
        }
        return self._client._make_request('POST', '/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs', json=data)

    def stop_job(self, job_id: int, strategy: str = "SoftStop") -> None:
        """
        Stop a running job.
        
        Args:
            job_id: The ID of the job to stop
            strategy: Stop strategy ("SoftStop" or "Kill")
        """
        data = {"strategy": strategy}
        self._client._make_request(
            'POST', 
            f'/odata/Jobs({job_id})/UiPath.Server.Configuration.OData.StopJob',
            json=data
        )

    def resume_job(self, job_id: int) -> None:
        """Resume a suspended job"""
        self._client._make_request(
            'POST',
            f'/odata/Jobs({job_id})/UiPath.Server.Configuration.OData.ResumeJob'
        )

    def get_job_logs(
        self,
        job_id: Optional[int] = None,
        robot_name: Optional[str] = None,
        level: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get logs for jobs with optional filters.
        
        Args:
            job_id: Filter by job ID
            robot_name: Filter by robot name
            level: Filter by log level (Trace, Info, Warn, Error)
            from_date: Filter logs after this date (ISO format)
            to_date: Filter logs before this date (ISO format)
        """
        filters = []
        if job_id:
            filters.append(f"JobId eq {job_id}")
        if robot_name:
            filters.append(f"RobotName eq '{robot_name}'")
        if level:
            filters.append(f"Level eq '{level}'")
        if from_date:
            filters.append(f"TimeStamp gt {from_date}")
        if to_date:
            filters.append(f"TimeStamp lt {to_date}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/RobotLogs', params=params) 
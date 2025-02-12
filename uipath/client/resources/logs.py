from typing import List, Dict
from ..base_client import BaseClient

class LogsClient:
    """Client for managing UiPath logs"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def submit_logs(self, logs: List[str]) -> None:
        """
        Inserts a collection of log entries.
        
        Args:
            logs: Collection of string representations of JSON log objects.
                 Example log entry:
                 {
                     "message": "Process execution started",
                     "level": "Information",
                     "timeStamp": "2023-01-18T14:46:07.4152893+02:00",
                     "windowsIdentity": "DESKTOP-1L50L0P\\WindowsUser",
                     "agentSessionId": "00000000-0000-0000-0000-000000000000",
                     "processName": "ProcessName",
                     "fileName": "Main",
                     "jobId": "8066c309-cef8-4b47-9163-b273fc14cc43"
                 }
        """
        self._client._make_request(
            'POST',
            '/api/Logs/SubmitLogs',
            json=logs
        )

    def post_log(self, log_data: Dict) -> None:
        """
        Inserts a single log entry.
        DEPRECATED: Use submit_logs instead.
        
        Args:
            log_data: Log entry data in JSON format
        """
        self._client._make_request(
            'POST',
            '/api/Logs',
            json=log_data
        ) 
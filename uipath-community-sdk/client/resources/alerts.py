from typing import Optional, Dict, List
from ..base_client import BaseClient

class AlertsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get alerts with optional filters.
        
        Args:
            severity: Filter by severity (Critical, Warning, Info)
            status: Filter by status (Active, Acknowledged, Resolved)
            from_date: Filter by date (ISO format)
        """
        filters = []
        if severity:
            filters.append(f"Severity eq '{severity}'")
        if status:
            filters.append(f"Status eq '{status}'")
        if from_date:
            filters.append(f"CreationTime gt {from_date}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/Alerts', params=params)

    def get_by_id(self, alert_id: int) -> Dict:
        """Get alert by ID"""
        return self._client._make_request('GET', f'/odata/Alerts({alert_id})')

    def acknowledge(self, alert_id: int, notes: Optional[str] = None) -> None:
        """
        Acknowledge an alert.
        
        Args:
            alert_id: ID of the alert
            notes: Optional acknowledgment notes
        """
        data = {"notes": notes} if notes else {}
        self._client._make_request(
            'POST',
            f'/odata/Alerts({alert_id})/UiPath.Server.Configuration.OData.Acknowledge',
            json=data
        )

    def resolve(self, alert_id: int, resolution: Optional[str] = None) -> None:
        """
        Resolve an alert.
        
        Args:
            alert_id: ID of the alert
            resolution: Optional resolution details
        """
        data = {"resolution": resolution} if resolution else {}
        self._client._make_request(
            'POST',
            f'/odata/Alerts({alert_id})/UiPath.Server.Configuration.OData.Resolve',
            json=data
        ) 
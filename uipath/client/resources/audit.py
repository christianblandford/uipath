from typing import Optional, Dict, List
from ..base_client import BaseClient

class AuditClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get_audit_logs(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        component: Optional[str] = None,
        action: Optional[str] = None
    ) -> List[Dict]:
        """
        Get audit logs with optional filters.
        
        Args:
            from_date: Start date for logs (ISO format)
            to_date: End date for logs (ISO format)
            component: Filter by component
            action: Filter by action type
        """
        filters = []
        if from_date:
            filters.append(f"CreationTime gt {from_date}")
        if to_date:
            filters.append(f"CreationTime lt {to_date}")
        if component:
            filters.append(f"Component eq '{component}'")
        if action:
            filters.append(f"Action eq '{action}'")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/AuditLogs', params=params)

    def get_audit_trail(
        self,
        entity_type: str,
        entity_id: int
    ) -> List[Dict]:
        """
        Get detailed audit trail for a specific entity.
        
        Args:
            entity_type: Type of entity
            entity_id: ID of the entity
        """
        params = {
            "entityType": entity_type,
            "entityId": entity_id
        }
        return self._client._make_request(
            'GET',
            '/odata/AuditLogs/UiPath.Server.Configuration.OData.GetAuditTrail',
            params=params
        )

    def export_audit_logs(
        self,
        from_date: str,
        to_date: str,
        format: str = "CSV"
    ) -> bytes:
        """
        Export audit logs to a file.
        
        Args:
            from_date: Start date for export
            to_date: End date for export
            format: Export format ("CSV" or "JSON")
        """
        params = {
            "from": from_date,
            "to": to_date,
            "format": format
        }
        return self._client._make_request(
            'GET',
            '/odata/AuditLogs/UiPath.Server.Configuration.OData.Export',
            params=params,
            raw_response=True
        ).content 
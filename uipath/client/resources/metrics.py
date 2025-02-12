from typing import Optional, Dict, List
from ..base_client import BaseClient

class MetricsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get_metrics(
        self,
        category: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict:
        """
        Get system metrics with optional filters.
        
        Args:
            category: Filter by metric category
            from_date: Start date for metrics (ISO format)
            to_date: End date for metrics (ISO format)
        """
        params = {}
        if category:
            params["category"] = category
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self._client._make_request('GET', '/api/Metrics', params=params)

    def get_performance_metrics(self) -> Dict:
        """Get performance-specific metrics"""
        return self._client._make_request('GET', '/api/Metrics/Performance')

    def get_resource_metrics(self) -> Dict:
        """Get resource utilization metrics"""
        return self._client._make_request('GET', '/api/Metrics/Resources') 
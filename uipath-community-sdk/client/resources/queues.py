from typing import Optional, Dict, List
from ..base_client import BaseClient

class QueuesClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(self, name: Optional[str] = None) -> List[Dict]:
        """
        Get queues. If name is provided, filter by name.
        """
        params = {"$filter": f"Name eq '{name}'"} if name else None
        return self._client._make_request('GET', '/odata/QueueDefinitions', params=params)

    def get_by_id(self, queue_id: int) -> Dict:
        """Get queue by ID"""
        return self._client._make_request('GET', f'/odata/QueueDefinitions({queue_id})')

    def create(self, queue_data: Dict) -> Dict:
        """Create new queue"""
        return self._client._make_request('POST', '/odata/QueueDefinitions', json=queue_data)

    def update(self, queue_id: int, queue_data: Dict) -> Dict:
        """Update existing queue"""
        return self._client._make_request('PUT', f'/odata/QueueDefinitions({queue_id})', json=queue_data)

    def delete(self, queue_id: int) -> None:
        """Delete queue"""
        self._client._make_request('DELETE', f'/odata/QueueDefinitions({queue_id})')

    # Queue Items operations
    def add_queue_item(self, queue_name: str, item_data: Dict) -> Dict:
        """
        Add a queue item to a specific queue
        """
        data = {
            "itemData": item_data,
            "name": queue_name
        }
        return self._client._make_request('POST', '/odata/Queues/UiPathODataSvc.AddQueueItem', json=data)

    def get_queue_items(
        self, 
        queue_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Get queue items, optionally filtered by queue name and status
        """
        filters = []
        if queue_name:
            filters.append(f"QueueDefinitionName eq '{queue_name}'")
        if status:
            filters.append(f"Status eq '{status}'")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/QueueItems', params=params)

    def set_transaction_status(
        self, 
        queue_item_id: int, 
        status: str,
        reason: Optional[str] = None
    ) -> Dict:
        """
        Set the status of a queue item (Success, Failed, Retried)
        """
        data = {
            "status": status,
            "reason": reason
        }
        return self._client._make_request(
            'POST', 
            f'/odata/Queues/UiPathODataSvc.SetTransactionStatus(key={queue_item_id})',
            json=data
        )

    def bulk_add_queue_items(self, queue_name: str, items: List[Dict]) -> Dict:
        """
        Add multiple queue items at once
        """
        data = {
            "queueName": queue_name,
            "items": items
        }
        return self._client._make_request(
            'POST',
            '/odata/Queues/UiPathODataSvc.BulkAddQueueItems',
            json=data
        ) 
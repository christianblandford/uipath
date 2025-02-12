from typing import Optional, Dict, List
from ..base_client import BaseClient

class TestDataQueueClient:
    """Client for managing UiPath Test Data Queues"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def add_item(self, queue_name: str, content: Dict) -> Dict:
        """
        Add a new test data queue item.
        
        Args:
            queue_name: Name of the queue
            content: Item content
            
        Returns:
            Created queue item
        """
        data = {
            "QueueName": queue_name,
            "Content": content
        }
        return self._client._make_request(
            'POST',
            '/api/TestDataQueueActions/AddItem',
            json=data
        )

    def bulk_add_items(self, queue_name: str, items: List[Dict]) -> int:
        """
        Bulk adds multiple queue items.
        
        Args:
            queue_name: Name of the queue
            items: List of item contents
            
        Returns:
            Number of items added
        """
        data = {
            "QueueName": queue_name,
            "Items": items
        }
        return self._client._make_request(
            'POST',
            '/api/TestDataQueueActions/BulkAddItems',
            json=data
        )

    def delete_all_items(self, queue_name: str) -> None:
        """
        Delete all items from a test data queue.
        
        Args:
            queue_name: Name of the queue to clear
        """
        params = {"queueName": queue_name}
        self._client._make_request(
            'DELETE',
            '/api/TestDataQueueActions/DeleteAllItems',
            params=params
        ) 
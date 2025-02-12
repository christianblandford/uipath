from typing import Optional, Dict, List, Union
from ..base_client import BaseClient

class WebhooksClient:
    """Client for managing UiPath Webhooks"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def create(self, webhook_data: Dict) -> Dict:
        """
        Create a new webhook.
        
        Args:
            webhook_data: Dict containing webhook details:
                - Name: Webhook name (required)
                - Description: Optional description
                - Url: Webhook URL (required)
                - Enabled: Whether webhook is enabled (required)
                - Secret: Optional secret for signature validation
                - SubscribeToAllEvents: Whether to subscribe to all events (required)
                - AllowInsecureSsl: Whether to allow insecure SSL (required)
                - Events: List of event types to subscribe to
                
        Returns:
            Created webhook details
        """
        return self._client._make_request(
            'POST',
            '/odata/Webhooks',
            json=webhook_data
        )

    def get(self, webhook_id: Optional[int] = None) -> Union[Dict, List[Dict]]:
        """
        Get webhook(s).
        
        Args:
            webhook_id: Optional webhook ID to get specific webhook
            
        Returns:
            Single webhook if ID provided, otherwise list of all webhooks
        """
        endpoint = f'/odata/Webhooks({webhook_id})' if webhook_id else '/odata/Webhooks'
        return self._client._make_request('GET', endpoint)

    def update(self, webhook_id: int, webhook_data: Dict) -> Dict:
        """
        Update an existing webhook.
        
        Args:
            webhook_id: ID of webhook to update
            webhook_data: Updated webhook data
            
        Returns:
            Updated webhook details
        """
        return self._client._make_request(
            'PUT',
            f'/odata/Webhooks({webhook_id})',
            json=webhook_data
        )

    def delete(self, webhook_id: int) -> None:
        """
        Delete a webhook.
        
        Args:
            webhook_id: ID of webhook to delete
        """
        self._client._make_request(
            'DELETE',
            f'/odata/Webhooks({webhook_id})'
        )

    def get_event_types(self) -> List[Dict]:
        """
        Get available webhook event types.
        
        Returns:
            List of available event types
        """
        return self._client._make_request('GET', '/odata/Webhooks/UiPath.Server.Configuration.OData.GetEventTypes')

    def ping(self, webhook_id: int) -> Dict:
        """
        Test a webhook by sending a ping event.
        
        Args:
            webhook_id: ID of webhook to test
            
        Returns:
            Ping test results
        """
        return self._client._make_request(
            'POST',
            f'/odata/Webhooks({webhook_id})/UiPath.Server.Configuration.OData.Ping'
        ) 
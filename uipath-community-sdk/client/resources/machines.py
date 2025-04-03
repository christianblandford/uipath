from typing import Optional, Dict, List
from ..base_client import BaseClient

class MachinesClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        is_online: Optional[bool] = None
    ) -> List[Dict]:
        """
        Get machines with optional filters.
        
        Args:
            name: Filter by machine name
            type: Filter by machine type (Standard, Template, etc.)
            is_online: Filter by online status
        """
        filters = []
        if name:
            filters.append(f"Name eq '{name}'")
        if type:
            filters.append(f"Type eq '{type}'")
        if is_online is not None:
            filters.append(f"IsOnline eq {str(is_online).lower()}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Machines', params=params)

    def get_by_id(self, machine_id: int) -> Dict:
        """Get machine by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Machines({machine_id})')

    def get_by_key(self, key: str) -> Dict:
        """Get machine by license key"""
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Machines/UiPath.Server.Configuration.OData.GetByKey(key=\'{key}\')'
        )

    def create(self, machine_data: Dict) -> Dict:
        """
        Create a new machine
        
        Args:
            machine_data: Dict containing machine details including:
                - Name: Machine name
                - Type: Machine type
                - NonProductionSlots: Number of non-production slots
                - UnattendedSlots: Number of unattended slots
                - Description: Optional description
        """
        return self._orchestrator._make_request('POST', '/odata/Machines', json=machine_data)

    def update(self, machine_id: int, machine_data: Dict) -> Dict:
        """
        Update an existing machine
        
        Args:
            machine_id: ID of the machine to update
            machine_data: Updated machine data
        """
        return self._orchestrator._make_request(
            'PUT',
            f'/odata/Machines({machine_id})',
            json=machine_data
        )

    def delete(self, machine_id: int) -> None:
        """Delete a machine"""
        return self._orchestrator._make_request('DELETE', f'/odata/Machines({machine_id})')

    def get_license_info(self, machine_id: int) -> Dict:
        """
        Get license information for a machine
        
        Args:
            machine_id: ID of the machine
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Machines({machine_id})/UiPath.Server.Configuration.OData.GetLicenseInfo'
        )

    def get_machine_settings(self, machine_id: int) -> Dict:
        """
        Get settings for a specific machine
        
        Args:
            machine_id: ID of the machine
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Machines({machine_id})/UiPath.Server.Configuration.OData.GetMachineSettings'
        )

    def update_machine_settings(self, machine_id: int, settings: Dict) -> None:
        """
        Update settings for a specific machine
        
        Args:
            machine_id: ID of the machine
            settings: Dict containing updated settings
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Machines({machine_id})/UiPath.Server.Configuration.OData.UpdateMachineSettings',
            json=settings
        )

    def get_robots(self, machine_id: int) -> List[Dict]:
        """
        Get all robots associated with a machine
        
        Args:
            machine_id: ID of the machine
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Machines({machine_id})/UiPath.Server.Configuration.OData.GetRobots'
        )

    def delete_by_key(self, key: str) -> None:
        """
        Delete a machine by its license key
        
        Args:
            key: Machine license key
        """
        return self._orchestrator._make_request(
            'DELETE',
            f'/odata/Machines/UiPath.Server.Configuration.OData.DeleteByKey(key=\'{key}\')'
        ) 
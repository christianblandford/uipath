from typing import Optional, Dict, List
from ..base_client import BaseClient

class RobotsClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

    def get(
        self,
        name: Optional[str] = None,
        machine_id: Optional[int] = None,
        type: Optional[str] = None,
        is_connected: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Get robots with optional filters.
        
        Args:
            name: Filter by robot name
            machine_id: Filter by machine ID
            type: Filter by robot type (Unattended, Attended, NonProduction, etc.)
            is_connected: Filter by connection status
            user_id: Filter by associated user ID
        """
        filters = []
        if name:
            filters.append(f"Name eq '{name}'")
        if machine_id:
            filters.append(f"MachineId eq {machine_id}")
        if type:
            filters.append(f"Type eq '{type}'")
        if is_connected is not None:
            filters.append(f"IsConnected eq {str(is_connected).lower()}")
        if user_id:
            filters.append(f"UserId eq {user_id}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._orchestrator._make_request('GET', '/odata/Robots', params=params)

    def get_by_id(self, robot_id: int) -> Dict:
        """Get robot by ID"""
        return self._orchestrator._make_request('GET', f'/odata/Robots({robot_id})')

    def create(self, robot_data: Dict) -> Dict:
        """
        Create a new robot
        
        Args:
            robot_data: Dict containing robot details including:
                - Name: Robot name
                - MachineId: Associated machine ID
                - Type: Robot type (Unattended, Attended, NonProduction)
                - Username: Associated Windows username
                - Password: Windows password (optional)
                - Description: Optional description
        """
        return self._orchestrator._make_request('POST', '/odata/Robots', json=robot_data)

    def update(self, robot_id: int, robot_data: Dict) -> Dict:
        """
        Update an existing robot
        
        Args:
            robot_id: ID of the robot to update
            robot_data: Updated robot data
        """
        return self._orchestrator._make_request(
            'PUT',
            f'/odata/Robots({robot_id})',
            json=robot_data
        )

    def delete(self, robot_id: int) -> None:
        """Delete a robot"""
        return self._orchestrator._make_request('DELETE', f'/odata/Robots({robot_id})')

    def get_license(self, robot_id: int) -> Dict:
        """
        Get license information for a robot
        
        Args:
            robot_id: ID of the robot
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.GetRobotLicense'
        )

    def toggle_enabled(self, robot_id: int, enabled: bool) -> None:
        """
        Enable or disable a robot
        
        Args:
            robot_id: ID of the robot
            enabled: Whether to enable or disable the robot
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.SetEnabled',
            json={"enabled": enabled}
        )

    def get_sessions(self, robot_id: int) -> List[Dict]:
        """
        Get active sessions for a robot
        
        Args:
            robot_id: ID of the robot
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.GetSessions'
        )

    def get_status(self, robot_id: int) -> Dict:
        """
        Get current status of a robot
        
        Args:
            robot_id: ID of the robot
        """
        return self._orchestrator._make_request(
            'GET',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.GetStatus'
        )

    def update_user(self, robot_id: int, user_data: Dict) -> None:
        """
        Update robot user credentials
        
        Args:
            robot_id: ID of the robot
            user_data: Dict containing:
                - Username: Windows username
                - Password: Windows password
        """
        return self._orchestrator._make_request(
            'POST',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.UpdateUser',
            json=user_data
        )

    def get_machine_name_by_id(self, robot_id: int) -> str:
        """
        Get machine name for a robot
        
        Args:
            robot_id: ID of the robot
        """
        response = self._orchestrator._make_request(
            'GET',
            f'/odata/Robots({robot_id})/UiPath.Server.Configuration.OData.GetMachineName'
        )
        return response.get('MachineName') 
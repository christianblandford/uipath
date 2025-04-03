from typing import Optional, Dict, List
from ..base_client import BaseClient

class UsersClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Dict]:
        """
        Get users with optional filters.
        
        Args:
            username: Filter by username
            email: Filter by email
            is_active: Filter by active status
        """
        filters = []
        if username:
            filters.append(f"UserName eq '{username}'")
        if email:
            filters.append(f"EmailAddress eq '{email}'")
        if is_active is not None:
            filters.append(f"IsActive eq {str(is_active).lower()}")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/Users', params=params)

    def get_by_id(self, user_id: int) -> Dict:
        """Get user by ID"""
        return self._client._make_request('GET', f'/odata/Users({user_id})')

    def create(self, user_data: Dict) -> Dict:
        """
        Create a new user.
        
        Args:
            user_data: Dict containing user details including:
                - UserName: Username
                - Password: Password
                - EmailAddress: Email address
                - Name: Full name
                - Type: User type
        """
        return self._client._make_request('POST', '/odata/Users', json=user_data)

    def update(self, user_id: int, user_data: Dict) -> Dict:
        """
        Update an existing user.
        
        Args:
            user_id: ID of user to update
            user_data: Updated user data
        """
        return self._client._make_request(
            'PUT',
            f'/odata/Users({user_id})',
            json=user_data
        )

    def delete(self, user_id: int) -> None:
        """Delete a user"""
        self._client._make_request('DELETE', f'/odata/Users({user_id})')

    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> None:
        """
        Change user password.
        
        Args:
            user_id: ID of the user
            current_password: Current password
            new_password: New password
        """
        data = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        self._client._make_request(
            'POST',
            f'/odata/Users({user_id})/UiPath.Server.Configuration.OData.ChangePassword',
            json=data
        ) 
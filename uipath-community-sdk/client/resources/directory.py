from typing import Optional, Dict, List
from ..base_client import BaseClient

class DirectoryClient:
    """Client for managing UiPath Directory Service operations"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def get_permissions(self, username: Optional[str] = None, domain: Optional[str] = None) -> List[Dict]:
        """
        Gets directory permissions.
        
        Args:
            username: Optional username to filter permissions
            domain: Optional domain to filter permissions
            
        Returns:
            List of directory permissions
        """
        params = {}
        if username:
            params["username"] = username
        if domain:
            params["domain"] = domain
            
        return self._client._make_request(
            'GET', 
            '/api/DirectoryService/GetDirectoryPermissions',
            params=params
        )

    def get_domains(self) -> List[Dict]:
        """
        Gets available domains.
        
        Returns:
            List of domain information
        """
        return self._client._make_request('GET', '/api/DirectoryService/GetDomains')

    def get_domain_user_id(
        self,
        domain: str,
        directory_identifier: str,
        user_name: str,
        user_type: str
    ) -> int:
        """
        Gets an orchestrator user Id by searching for the domain user information.
        
        Args:
            domain: The domain name
            directory_identifier: Directory identifier
            user_name: Username to search for
            user_type: Type of user (User, Robot, DirectoryUser, etc)
            
        Returns:
            User ID
        """
        params = {
            "domain": domain,
            "directoryIdentifier": directory_identifier,
            "userName": user_name,
            "userType": user_type
        }
        return self._client._make_request(
            'GET',
            '/api/DirectoryService/GetDomainUserId',
            params=params
        )

    def search_users_and_groups(
        self,
        search_context: str,
        domain: str,
        prefix: str
    ) -> List[Dict]:
        """
        Search for users and groups in the directory.
        
        Args:
            search_context: Context to search in (All, Users, Groups, etc)
            domain: Domain to search in
            prefix: Search prefix/term
            
        Returns:
            List of matching users/groups
        """
        params = {
            "searchContext": search_context,
            "domain": domain,
            "prefix": prefix
        }
        return self._client._make_request(
            'GET',
            '/api/DirectoryService/SearchForUsersAndGroups',
            params=params
        ) 
from typing import Optional, Dict, List
from ..base_client import BaseClient

class FoldersClient:
    """Client for managing UiPath Folders"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def delete(self, key: str) -> None:
        """
        Deletes a folder. Succeeds only if no entities or user associations
        exist in this folder or any of its descendants.
        
        Args:
            key: The folder key to delete
        """
        params = {"key": key}
        self._client._make_request('DELETE', '/api/Folders/DeleteByKey', params=params)

    def get_all_for_current_user(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None
    ) -> Dict:
        """
        Returns a subset (paginated) of the folders the current user has access to.
        
        Args:
            take: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Paginated list of folders
        """
        params = {}
        if take is not None:
            params["take"] = take
        if skip is not None:
            params["skip"] = skip
            
        return self._client._make_request(
            'GET',
            '/api/Folders/GetAllForCurrentUser',
            params=params
        )

    def update_name_description(
        self,
        key: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """
        Updates a folder's name and/or description.
        
        Args:
            key: Folder key to update
            name: New folder name
            description: New folder description
        """
        data = {}
        if name:
            data["Name"] = name
        if description:
            data["Description"] = description
            
        params = {"key": key}
        self._client._make_request(
            'PATCH',
            '/api/Folders/PatchNameDescription',
            params=params,
            json=data
        )

    def get(self, search_text: Optional[str] = None, folder_type: Optional[str] = None) -> List[Dict]:
        """
        Get folders with optional filters.
        
        Args:
            search_text: Filter folders by name
            folder_type: Filter by folder type ("Standard", "Personal", "Virtual", "Solution")
        """
        params = {}
        if search_text:
            params["searchText"] = search_text
        if folder_type:
            params["folderTypes"] = [folder_type]
            
        return self._client._make_request(
            'GET', 
            '/api/FoldersNavigation/GetFoldersForCurrentUser',
            params=params
        )

    def get_by_id(self, folder_id: int) -> Dict:
        """
        Get folder navigation context by ID
        """
        params = {"folderId": folder_id}
        return self._client._make_request(
            'GET',
            '/api/FoldersNavigation/GetFolderNavigationContextForCurrentUser',
            params=params
        )

    def get_folder_hierarchy(self) -> List[Dict]:
        """
        Returns the complete folder hierarchy the current user has access to
        """
        return self._client._make_request(
            'GET',
            '/api/FoldersNavigation/GetAllFoldersForCurrentUser'
        )

    def get_user_folder_roles(
        self,
        username: str,
        user_type: str = "User",
        search_text: Optional[str] = None,
        skip: int = 0,
        take: int = 100
    ) -> Dict:
        """
        Get folder roles for a specific user
        
        Args:
            username: The username to get roles for
            user_type: Type of user ("User", "Group", "Machine", "Robot", "ExternalApplication")
            search_text: Filter by folder name
            skip: Number of records to skip
            take: Number of records to return
        """
        params = {
            "username": username,
            "type": user_type,
            "skip": skip,
            "take": take
        }
        if search_text:
            params["searchText"] = search_text
            
        return self._client._make_request(
            'GET',
            '/api/FoldersNavigation/GetAllRolesForUser',
            params=params
        ) 
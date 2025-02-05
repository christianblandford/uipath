from typing import Optional, Dict, List
from ..base_client import BaseClient

class FoldersClient:
    def __init__(self, orchestrator: BaseClient):
        self._orchestrator = orchestrator

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
            
        return self._orchestrator._make_request(
            'GET', 
            '/api/FoldersNavigation/GetFoldersForCurrentUser',
            params=params
        )

    def get_by_id(self, folder_id: int) -> Dict:
        """
        Get folder navigation context by ID
        """
        params = {"folderId": folder_id}
        return self._orchestrator._make_request(
            'GET',
            '/api/FoldersNavigation/GetFolderNavigationContextForCurrentUser',
            params=params
        )

    def get_folder_hierarchy(self) -> List[Dict]:
        """
        Returns the complete folder hierarchy the current user has access to
        """
        return self._orchestrator._make_request(
            'GET',
            '/api/FoldersNavigation/GetAllFoldersForCurrentUser'
        )

    def update(self, folder_key: str, folder_data: Dict) -> None:
        """
        Update folder name and description
        
        Args:
            folder_key: The UUID of the folder
            folder_data: Dict containing "Name" and/or "Description"
        """
        return self._orchestrator._make_request(
            'PATCH',
            f'/api/Folders/PatchNameDescription',
            params={"key": folder_key},
            json=folder_data
        )

    def delete(self, folder_key: str) -> None:
        """
        Delete a folder. Only succeeds if no entities or user associations exist.
        
        Args:
            folder_key: The UUID of the folder to delete
        """
        return self._orchestrator._make_request(
            'DELETE',
            '/api/Folders/DeleteByKey',
            params={"key": folder_key}
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
            
        return self._orchestrator._make_request(
            'GET',
            '/api/FoldersNavigation/GetAllRolesForUser',
            params=params
        ) 
from typing import Optional, Dict, List
from ..base_client import BaseClient

class TaskFormsClient:
    """Client for managing UiPath Task Forms"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def get(
        self,
        process_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Get task forms with optional filters.
        
        Args:
            process_name: Filter by process name
            status: Filter by form status (Pending, Completed, Canceled)
        """
        filters = []
        if process_name:
            filters.append(f"ProcessName eq '{process_name}'")
        if status:
            filters.append(f"Status eq '{status}'")
            
        params = {"$filter": " and ".join(filters)} if filters else None
        return self._client._make_request('GET', '/odata/TaskForms', params=params)

    def get_by_id(self, form_id: int) -> Dict:
        """Get task form by ID"""
        return self._client._make_request('GET', f'/odata/TaskForms({form_id})')

    def submit(self, form_id: int, data: Dict) -> None:
        """
        Submit a response to a task form.
        
        Args:
            form_id: ID of the form
            data: Form response data
        """
        self._client._make_request(
            'POST',
            f'/odata/TaskForms({form_id})/UiPath.Server.Configuration.OData.Submit',
            json=data
        )

    def assign(self, form_id: int, user_id: int) -> None:
        """
        Assign a task form to a user.
        
        Args:
            form_id: ID of the form
            user_id: ID of the user to assign
        """
        data = {"userId": user_id}
        self._client._make_request(
            'POST',
            f'/odata/TaskForms({form_id})/UiPath.Server.Configuration.OData.Assign',
            json=data
        )

    def get_tasks(
        self,
        title: Optional[str] = None,
        status: Optional[str] = None,
        assigned_to: Optional[int] = None,
        skip: int = 0,
        take: int = 100
    ) -> Dict:
        """
        Get task forms with optional filters.
        
        Args:
            title: Filter by task title
            status: Filter by task status (Unassigned, Pending, Completed)
            assigned_to: Filter by assigned user ID
            skip: Number of records to skip
            take: Number of records to return
            
        Returns:
            Paginated list of tasks
        """
        params = {
            "$skip": skip,
            "$take": take
        }
        filters = []
        if title:
            filters.append(f"Title eq '{title}'")
        if status:
            filters.append(f"Status eq '{status}'")
        if assigned_to:
            filters.append(f"AssignedToUserId eq {assigned_to}")
            
        if filters:
            params["$filter"] = " and ".join(filters)
            
        return self._client._make_request('GET', '/odata/Tasks', params=params)

    def get_task_by_id(self, task_id: int) -> Dict:
        """
        Get task form by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task details
        """
        return self._client._make_request('GET', f'/odata/Tasks({task_id})')

    def update_task(self, task_id: int, task_data: Dict) -> Dict:
        """
        Update a task form.
        
        Args:
            task_id: ID of task to update
            task_data: Updated task data
            
        Returns:
            Updated task details
        """
        return self._client._make_request(
            'PUT',
            f'/odata/Tasks({task_id})',
            json=task_data
        )

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task form.
        
        Args:
            task_id: ID of task to delete
        """
        self._client._make_request('DELETE', f'/odata/Tasks({task_id})')

    def complete_task(self, task_id: int, action: str) -> None:
        """
        Complete a task form with specified action.
        
        Args:
            task_id: ID of task to complete
            action: Action taken to complete the task
        """
        data = {"action": action}
        self._client._make_request(
            'POST',
            f'/odata/Tasks({task_id})/UiPath.Server.Configuration.OData.Complete',
            json=data
        ) 
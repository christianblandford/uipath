# Folders

The Folders resource allows you to manage organizational units in UiPath Orchestrator. Folders help organize resources and control access to processes, robots, and assets.

## Related Resources
- [Directory](directory.md) - User and group permissions for folders
- [Assets](assets.md) - Assets organized in folders
- [Robots](robots.md) - Robots assigned to folders
- [Processes](processes.md) - Processes organized in folders

## Methods

### get()
Get a list of folders with optional filters.

```python
folders = client.folders.get(
    display_name="Production",    # Filter by display name
    parent_id=123                # Filter by parent folder ID
)
```

#### Parameters
- `display_name` (str, optional): Filter by folder display name
- `parent_id` (int, optional): Filter by parent folder ID

#### Returns
List[Dict]: List of folder objects matching the filters

### get_by_id()
Get a specific folder by ID.

```python
folder = client.folders.get_by_id(123)
```

#### Parameters
- `folder_id` (int): ID of the folder to retrieve

#### Returns
Dict: Folder details

### create()
Create a new folder.

```python
folder = client.folders.create({
    "DisplayName": "Production",
    "Description": "Production environment resources",
    "ParentId": 123,  # Optional parent folder ID
    "ProvisionType": "Manual"
})
```

#### Parameters
- `folder_data` (Dict): Folder configuration including:
  - `DisplayName` (str, required): Folder name
  - `Description` (str, optional): Folder description
  - `ParentId` (int, optional): Parent folder ID
  - `ProvisionType` (str, optional): Provisioning type (Manual, Automatic)

#### Returns
Dict: Created folder details

### update()
Update an existing folder.

```python
client.folders.update(123, {
    "DisplayName": "Production-2023",
    "Description": "Updated production environment"
})
```

#### Parameters
- `folder_id` (int): ID of folder to update
- `folder_data` (Dict): Updated folder data

#### Returns
Dict: Updated folder details

### delete()
Delete a folder.

```python
client.folders.delete(123)
```

#### Parameters
- `folder_id` (int): ID of folder to delete

### assign_users()
Assign users to a folder.

```python
client.folders.assign_users(123, [
    {"UserId": 456, "RoleId": 789}
])
```

#### Parameters
- `folder_id` (int): ID of the folder
- `assignments` (List[Dict]): List of user-role assignments

### get_users()
Get users assigned to a folder.

```python
users = client.folders.get_users(123)
```

#### Parameters
- `folder_id` (int): ID of the folder

#### Returns
List[Dict]: List of users assigned to the folder

## Examples

### Folder Hierarchy Management

```python
def create_folder_structure(structure: dict, parent_id: Optional[int] = None):
    """Create a hierarchical folder structure"""
    created_folders = {}
    
    for name, subfolders in structure.items():
        # Create parent folder
        folder = client.folders.create({
            "DisplayName": name,
            "Description": f"Created as part of hierarchy",
            "ParentId": parent_id
        })
        created_folders[name] = folder
        
        # Create subfolders recursively
        if isinstance(subfolders, dict):
            subfolder_results = create_folder_structure(
                subfolders,
                parent_id=folder["Id"]
            )
            created_folders.update(subfolder_results)
    
    return created_folders

# Create folder hierarchy
structure = {
    "Production": {
        "Finance": {},
        "HR": {},
        "Operations": {
            "EMEA": {},
            "APAC": {},
            "Americas": {}
        }
    }
}
folders = create_folder_structure(structure)
```

### User Access Management

```python
def setup_folder_access(folder_id: int, user_assignments: List[Dict]):
    """Setup user access for a folder"""
    # Get current users
    current_users = client.folders.get_users(folder_id)
    
    # Remove existing assignments
    for user in current_users:
        client.folders.remove_user(
            folder_id=folder_id,
            user_id=user["UserId"]
        )
    
    # Add new assignments
    client.folders.assign_users(folder_id, user_assignments)
    
    return client.folders.get_users(folder_id)

# Setup folder access
assignments = [
    {"UserId": 123, "RoleId": 456},  # Admin role
    {"UserId": 789, "RoleId": 101}   # User role
]
users = setup_folder_access(folder_id=123, user_assignments=assignments)
```

### Resource Organization

```python
def organize_resources(folder_name: str):
    """Create and organize resources in a folder"""
    # Create folder
    folder = client.folders.create({
        "DisplayName": folder_name,
        "Description": "Organized resources folder"
    })
    
    # Create assets in folder
    asset = client.assets.create({
        "Name": f"{folder_name}_Config",
        "ValueType": "Text",
        "Value": "configuration",
        "FolderId": folder["Id"]
    })
    
    # Upload process to folder
    process = client.processes.upload(
        "Process.nupkg",
        folder_id=folder["Id"]
    )
    
    return {
        "folder": folder,
        "asset": asset,
        "process": process
    }

# Organize resources
resources = organize_resources("Project_A")
```

### Folder Cleanup

```python
def cleanup_empty_folders(parent_id: Optional[int] = None):
    """Remove empty folders"""
    folders = client.folders.get(parent_id=parent_id)
    
    for folder in folders:
        # Check for subfolders
        subfolders = client.folders.get(parent_id=folder["Id"])
        if subfolders:
            cleanup_empty_folders(folder["Id"])
        
        # Check if folder is empty
        assets = client.assets.get(folder_id=folder["Id"])
        processes = client.processes.get(folder_id=folder["Id"])
        robots = client.robots.get(folder_id=folder["Id"])
        
        if not (assets or processes or robots or subfolders):
            print(f"Deleting empty folder: {folder['DisplayName']}")
            client.folders.delete(folder["Id"])

# Clean up empty folders
cleanup_empty_folders()
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to delete non-empty folder
    client.folders.delete(123)
except HTTPError as e:
    if e.response.status_code == 409:
        print("Cannot delete non-empty folder")
    elif e.response.status_code == 404:
        print("Folder not found")
    else:
        print(f"Error managing folder: {e}")
```

## Best Practices

1. Use consistent naming conventions
2. Implement logical hierarchy
3. Control folder access carefully
4. Document folder structure
5. Regular access audits
6. Clean up unused folders
7. Maintain folder organization
8. Use descriptive folder names
9. Consider resource relationships

## Security Considerations

1. Implement proper access controls
2. Regular permission audits
3. Monitor folder access
4. Secure sensitive resources
5. Document access policies
6. Control folder creation
7. Maintain audit trails

## See Also
- [UiPath Folders Documentation](https://docs.uipath.com/orchestrator/docs/about-folders)
- [Folder Management](https://docs.uipath.com/orchestrator/docs/managing-folders)
- [Folder Security](https://docs.uipath.com/orchestrator/docs/folder-security)
- [Directory](directory.md) for user management
- [Assets](assets.md) for resource management 
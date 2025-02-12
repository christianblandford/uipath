# Directory

The Directory resource allows you to manage users, groups, and roles in UiPath Orchestrator. It provides functionality for user authentication, authorization, and organizational structure management.

## Related Resources
- [Robots](robots.md) - Robots associated with users
- [Assets](assets.md) - Assets with user-specific permissions
- [Folders](folders.md) - Folders with user access controls

## Methods

### get_users()
Get a list of users with optional filters.

```python
users = client.directory.get_users(
    username="john.doe",     # Filter by username
    email="john@example.com" # Filter by email
)
```

#### Parameters
- `username` (str, optional): Filter by username
- `email` (str, optional): Filter by email address

#### Returns
List[Dict]: List of user objects matching the filters

### get_user_by_id()
Get a specific user by ID.

```python
user = client.directory.get_user_by_id(123)
```

#### Parameters
- `user_id` (int): ID of the user to retrieve

#### Returns
Dict: User details

### get_domains()
Get available authentication domains.

```python
domains = client.directory.get_domains()
```

#### Returns
List[Dict]: List of available domains

### search_users_and_groups()
Search for users and groups.

```python
results = client.directory.search_users_and_groups(
    search_context="Users",    # Search context (Users, Groups)
    domain="mydomain",        # Domain to search in
    prefix="john"            # Search prefix
)
```

#### Parameters
- `search_context` (str): Context to search in (Users, Groups)
- `domain` (str): Domain to search in
- `prefix` (str): Search prefix

#### Returns
List[Dict]: Search results

### get_permissions()
Get permissions for a user.

```python
permissions = client.directory.get_permissions(
    username="john.doe",
    domain="mydomain"
)
```

#### Parameters
- `username` (str): Username to check permissions for
- `domain` (str): User's domain

#### Returns
Dict: User permissions

### assign_role()
Assign a role to a user.

```python
client.directory.assign_role(
    user_id=123,
    role_id=456
)
```

#### Parameters
- `user_id` (int): ID of the user
- `role_id` (int): ID of the role to assign

### remove_role()
Remove a role from a user.

```python
client.directory.remove_role(
    user_id=123,
    role_id=456
)
```

#### Parameters
- `user_id` (int): ID of the user
- `role_id` (int): ID of the role to remove

## Examples

### User Management

```python
# Search for users
users = client.directory.search_users_and_groups(
    search_context="Users",
    domain="mydomain",
    prefix="john"
)

# Get user details and permissions
for user in users:
    permissions = client.directory.get_permissions(
        username=user["Username"],
        domain=user["Domain"]
    )
    print(f"User: {user['Username']}")
    print(f"Permissions: {permissions}")
```

### Role Assignment

```python
def setup_user_roles(username: str, domain: str, roles: List[int]):
    # Find user
    users = client.directory.search_users_and_groups(
        search_context="Users",
        domain=domain,
        prefix=username
    )
    
    if not users:
        raise ValueError(f"User {username} not found")
    
    user = users[0]
    
    # Get current permissions
    current_perms = client.directory.get_permissions(
        username=user["Username"],
        domain=user["Domain"]
    )
    
    # Remove existing roles
    for role in current_perms.get("Roles", []):
        client.directory.remove_role(
            user_id=user["Id"],
            role_id=role["Id"]
        )
    
    # Assign new roles
    for role_id in roles:
        client.directory.assign_role(
            user_id=user["Id"],
            role_id=role_id
        )

# Setup roles for user
setup_user_roles(
    username="john.doe",
    domain="mydomain",
    roles=[123, 456]  # Role IDs
)
```

### Domain Management

```python
def validate_domain_access():
    # Get available domains
    domains = client.directory.get_domains()
    
    # Check each domain
    results = {}
    for domain in domains:
        try:
            # Try to search in domain
            users = client.directory.search_users_and_groups(
                search_context="Users",
                domain=domain["Name"],
                prefix="test"
            )
            results[domain["Name"]] = "accessible"
        except Exception as e:
            results[domain["Name"]] = f"error: {str(e)}"
    
    return results

# Check domain access
domain_status = validate_domain_access()
```

### User Permission Audit

```python
def audit_user_permissions(username: str, domain: str):
    # Get user permissions
    permissions = client.directory.get_permissions(
        username=username,
        domain=domain
    )
    
    # Analyze permissions
    audit_results = {
        "username": username,
        "domain": domain,
        "roles": permissions.get("Roles", []),
        "permissions": permissions.get("Permissions", []),
        "timestamp": datetime.now().isoformat()
    }
    
    # Log audit results
    with open("permission_audit.log", "a") as f:
        f.write(json.dumps(audit_results) + "\n")
    
    return audit_results

# Audit user permissions
audit = audit_user_permissions("john.doe", "mydomain")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to get permissions for non-existent user
    client.directory.get_permissions(
        username="nonexistent",
        domain="mydomain"
    )
except HTTPError as e:
    if e.response.status_code == 404:
        print("User not found")
    elif e.response.status_code == 403:
        print("Permission denied")
    else:
        print(f"Error checking permissions: {e}")
```

## Best Practices

1. Use domain-qualified usernames
2. Implement role-based access control
3. Regularly audit user permissions
4. Remove unused roles and permissions
5. Document role assignments
6. Use group-based permissions where possible
7. Regular permission reviews
8. Monitor permission changes
9. Maintain user lifecycle management

## Security Considerations

1. Principle of least privilege
2. Regular access reviews
3. Monitor failed authentication attempts
4. Audit permission changes
5. Secure role management
6. Password policy enforcement
7. User activity monitoring

## See Also
- [UiPath Directory Documentation](https://docs.uipath.com/orchestrator/docs/managing-users)
- [Role-Based Access Control](https://docs.uipath.com/orchestrator/docs/about-role-based-access)
- [Security Best Practices](https://docs.uipath.com/orchestrator/docs/security-best-practices)
- [Robots](robots.md) for robot-user associations
- [Assets](assets.md) for permission-controlled assets 
# Releases

The Releases resource allows you to manage UiPath process releases. Releases represent specific versions of processes that can be deployed and executed by robots.

## Related Resources
- [Processes](processes.md) - Processes that are released
- [Jobs](jobs.md) - Jobs that execute releases
- [Robots](robots.md) - Robots that run releases
- [Packages](packages.md) - Package files used in releases

## Methods

### get()
Get a list of releases with optional filters.

```python
releases = client.releases.get(
    process_key="MyProcess",     # Filter by process key
    is_latest=True,             # Filter for latest versions
    environment_id=123          # Filter by environment
)
```

#### Parameters
- `process_key` (str, optional): Filter by process key
- `is_latest` (bool, optional): Filter for latest versions only
- `environment_id` (int, optional): Filter by environment ID

#### Returns
List[Dict]: List of release objects matching the filters

### get_by_id()
Get a specific release by ID.

```python
release = client.releases.get_by_id(123)
```

#### Parameters
- `release_id` (int): ID of the release to retrieve

#### Returns
Dict: Release details

### get_by_key()
Get a release by its key.

```python
release = client.releases.get_by_key("release-key-123")
```

#### Parameters
- `key` (str): Release key

#### Returns
Dict: Release details

### create()
Create a new release.

```python
release = client.releases.create({
    "Name": "MyProcess Release",
    "ProcessKey": "MyProcess",
    "ProcessVersion": "1.0.0",
    "Description": "Production release",
    "EnvironmentId": 123,
    "EntryPointId": "Main"
})
```

#### Parameters
- `release_data` (Dict): Release configuration including:
  - `Name` (str, required): Release name
  - `ProcessKey` (str, required): Process identifier
  - `ProcessVersion` (str, required): Version string
  - `Description` (str, optional): Release description
  - `EnvironmentId` (int, optional): Target environment ID
  - `EntryPointId` (str, optional): Process entry point

#### Returns
Dict: Created release details

### update()
Update an existing release.

```python
client.releases.update(123, {
    "Name": "Updated Release Name",
    "Description": "Updated description"
})
```

#### Parameters
- `release_id` (int): ID of release to update
- `release_data` (Dict): Updated release data

#### Returns
Dict: Updated release details

### delete()
Delete a release by ID.

```python
client.releases.delete(123)
```

#### Parameters
- `release_id` (int): ID of release to delete

### delete_by_key()
Delete a release by key.

```python
client.releases.delete_by_key("release-key-123")
```

#### Parameters
- `key` (str): Release key to delete

### update_process_settings()
Update process settings for a release.

```python
client.releases.update_process_settings(123, {
    "MaxConcurrentJobs": 5,
    "JobPriority": "Normal",
    "AutoUpdate": True
})
```

#### Parameters
- `release_id` (int): ID of the release
- `settings` (Dict): Process settings

#### Returns
Dict: Updated settings

### get_latest_version()
Get the latest version of a release for a specific process.

```python
latest = client.releases.get_latest_version(
    process_key="MyProcess",
    environment_id=123
)
```

#### Parameters
- `process_key` (str): Process identifier
- `environment_id` (int, optional): Environment ID filter

#### Returns
Dict: Latest release details

## Examples

### Release Management Workflow

```python
# Create release from process
def create_release_from_process(process_key: str, version: str, environment_id: int):
    release = client.releases.create({
        "Name": f"{process_key} v{version}",
        "ProcessKey": process_key,
        "ProcessVersion": version,
        "EnvironmentId": environment_id,
        "Description": f"Release of {process_key} version {version}"
    })
    
    # Configure process settings
    client.releases.update_process_settings(
        release["Id"],
        {
            "MaxConcurrentJobs": 3,
            "JobPriority": "Normal",
            "AutoUpdate": False
        }
    )
    
    return release

# Create releases for different environments
dev_release = create_release_from_process("MyProcess", "1.0.0", dev_env_id)
prod_release = create_release_from_process("MyProcess", "1.0.0", prod_env_id)
```

### Version Control

```python
def manage_releases(process_key: str):
    # Get all releases for process
    releases = client.releases.get(process_key=process_key)
    
    # Get latest release
    latest = client.releases.get_latest_version(process_key)
    
    # Archive old releases
    for release in releases:
        if release["Id"] != latest["Id"]:
            # Archive release data
            archived_data = {
                "Name": f"Archived_{release['Name']}",
                "Description": f"Archived on {datetime.now()}"
            }
            client.releases.update(release["Id"], archived_data)

# Manage releases
manage_releases("MyProcess")
```

### Environment Promotion

```python
def promote_to_production(release_key: str):
    # Get release details
    release = client.releases.get_by_key(release_key)
    
    # Create production release
    prod_release = client.releases.create({
        "Name": f"{release['Name']}_Production",
        "ProcessKey": release["ProcessKey"],
        "ProcessVersion": release["ProcessVersion"],
        "EnvironmentId": prod_environment_id,
        "Description": f"Production release promoted from {release_key}"
    })
    
    # Copy process settings
    settings = client.releases.get_process_settings(release["Id"])
    client.releases.update_process_settings(prod_release["Id"], settings)
    
    return prod_release

# Promote release to production
prod_release = promote_to_production("dev-release-key-123")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create release with invalid process key
    client.releases.create({
        "Name": "Invalid Release",
        "ProcessKey": "NonExistentProcess",
        "ProcessVersion": "1.0.0"
    })
except HTTPError as e:
    if e.response.status_code == 404:
        print("Process not found")
    elif e.response.status_code == 400:
        print("Invalid release configuration")
    else:
        print(f"Error creating release: {e}")
```

## Best Practices

1. Use consistent naming conventions for releases
2. Include version information in release names
3. Provide detailed descriptions for releases
4. Configure appropriate process settings per environment
5. Archive or delete obsolete releases
6. Test releases in development before production
7. Document release dependencies
8. Maintain release history
9. Use environment-specific configurations

## Security Considerations

1. Control access to release management
2. Audit release changes
3. Secure release configurations
4. Review process settings before deployment
5. Monitor release execution permissions
6. Validate release configurations

## See Also
- [UiPath Release Documentation](https://docs.uipath.com/orchestrator/docs/about-releases)
- [Release Management](https://docs.uipath.com/orchestrator/docs/managing-releases)
- [Release Security](https://docs.uipath.com/orchestrator/docs/release-security)
- [Processes](processes.md) for process management
- [Jobs](jobs.md) for release execution 
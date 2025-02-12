# Processes

The Processes resource allows you to manage UiPath automation processes (packages) in Orchestrator. Processes are the automation projects that can be executed by robots.

## Related Resources
- [Releases](releases.md) - Process versions that can be deployed
- [Jobs](jobs.md) - Process executions
- [Robots](robots.md) - Robots that execute processes
- [Packages](packages.md) - Process package files
- [Assets](assets.md) - Configuration used by processes

## Methods

### get()
Get a list of processes with optional filters.

```python
processes = client.processes.get(
    is_active=True,           # Filter by active status
    is_latest=True,          # Filter for latest versions
    package_key="MyProcess"  # Filter by package key
)
```

#### Parameters
- `is_active` (bool, optional): Filter by active status
- `is_latest` (bool, optional): Filter for latest versions only
- `package_key` (str, optional): Filter by package key

#### Returns
List[Dict]: List of process objects matching the filters

### get_by_id()
Get a specific process by ID.

```python
process = client.processes.get_by_id(123)
```

#### Parameters
- `process_id` (int): ID of the process to retrieve

#### Returns
Dict: Process details

### get_by_key()
Get a process by its package key.

```python
process = client.processes.get_by_key("MyProcess")
```

#### Parameters
- `key` (str): Package key of the process

#### Returns
Dict: Process details

### upload()
Upload a new process package (.nupkg file).

```python
process = client.processes.upload(
    file_path="MyProcess.1.0.0.nupkg",
    version="1.0.0"  # Optional
)
```

#### Parameters
- `file_path` (str): Path to the .nupkg file
- `version` (str, optional): Version string for the package

#### Returns
Dict: Uploaded process details

### upload_stream()
Upload a process package from a file stream.

```python
with open("MyProcess.nupkg", "rb") as f:
    process = client.processes.upload_stream(
        file_stream=f,
        filename="MyProcess.nupkg",
        version="1.0.0"
    )
```

#### Parameters
- `file_stream` (BinaryIO): File-like object containing the package
- `filename` (str): Name of the file
- `version` (str, optional): Version string for the package

#### Returns
Dict: Uploaded process details

### download()
Download a process package.

```python
package_content = client.processes.download(123)
with open("MyProcess.nupkg", "wb") as f:
    f.write(package_content)
```

#### Parameters
- `process_id` (int): ID of the process to download

#### Returns
bytes: The process package content

### delete()
Delete a process.

```python
client.processes.delete(123)
```

#### Parameters
- `process_id` (int): ID of the process to delete

### set_active()
Set the active status of a process.

```python
client.processes.set_active(123, True)
```

#### Parameters
- `process_id` (int): ID of the process
- `is_active` (bool): Whether the process should be active

## Examples

### Managing Process Lifecycle

```python
# Upload new process
process = client.processes.upload("MyProcess.1.0.0.nupkg")

# Create a release for the process
release = client.releases.create({
    "Name": "MyProcess Release",
    "ProcessKey": process["Key"],
    "ProcessVersion": process["Version"],
    "Description": "Initial release"
})

# Start a job using the process
job = client.jobs.start_jobs(
    release_key=release["Key"],
    robot_ids=[123],
    input_arguments={
        "InputParam": "value"
    }
)
```

### Version Management

```python
# Get all versions of a process
versions = client.processes.get(package_key="MyProcess")

# Get only latest version
latest = client.processes.get(
    package_key="MyProcess",
    is_latest=True
)[0]

# Upload new version
new_version = client.processes.upload(
    "MyProcess.2.0.0.nupkg",
    version="2.0.0"
)

# Deactivate old version
client.processes.set_active(versions[0]["Id"], False)
```

### Process Deployment

```python
import os
from datetime import datetime

def deploy_process(package_path: str, environment: str):
    # Upload process
    process = client.processes.upload(package_path)
    
    # Create release
    release = client.releases.create({
        "Name": f"{process['Key']}_{environment}",
        "ProcessKey": process["Key"],
        "ProcessVersion": process["Version"],
        "Description": f"Deployed to {environment} on {datetime.now()}"
    })
    
    # Configure process settings
    settings = {
        "MaxConcurrentJobs": 5,
        "JobPriority": "Normal",
        "AutoUpdate": True
    }
    client.releases.update_process_settings(release["Id"], settings)
    
    return release

# Deploy to different environments
dev_release = deploy_process("MyProcess.nupkg", "Development")
prod_release = deploy_process("MyProcess.nupkg", "Production")
```

### Package Management

```python
def archive_old_versions(process_key: str, keep_versions: int = 3):
    # Get all versions
    versions = client.processes.get(package_key=process_key)
    versions.sort(key=lambda x: x["Version"], reverse=True)
    
    # Keep the latest n versions
    for old_version in versions[keep_versions:]:
        # Download for archival
        content = client.processes.download(old_version["Id"])
        archive_path = f"archive/{process_key}_{old_version['Version']}.nupkg"
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        
        with open(archive_path, "wb") as f:
            f.write(content)
            
        # Delete from Orchestrator
        client.processes.delete(old_version["Id"])
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to upload invalid package
    client.processes.upload("invalid.nupkg")
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid package format")
    elif e.response.status_code == 409:
        print("Package version conflict")
    else:
        print(f"Error uploading package: {e}")
```

## Best Practices

1. Use semantic versioning for process packages
2. Keep process names consistent across environments
3. Document process dependencies and requirements
4. Test processes in development environment before production
5. Archive old versions before deletion
6. Use meaningful descriptions for process versions
7. Configure appropriate process settings for each environment
8. Monitor process execution statistics
9. Maintain process documentation

## Security Considerations

1. Control access to process uploads
2. Audit process modifications
3. Secure process input arguments
4. Review process dependencies
5. Monitor process execution permissions
6. Validate process packages before deployment

## See Also
- [UiPath Process Documentation](https://docs.uipath.com/orchestrator/docs/about-processes)
- [Package Management](https://docs.uipath.com/orchestrator/docs/managing-packages)
- [Process Security](https://docs.uipath.com/orchestrator/docs/process-security)
- [Releases](releases.md) for version management
- [Jobs](jobs.md) for process execution 
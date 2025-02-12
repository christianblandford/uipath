# Packages

The Packages resource allows you to manage UiPath process packages (.nupkg files) in Orchestrator. Packages contain the automation projects that can be deployed and executed by robots.

## Related Resources
- [Processes](processes.md) - Processes using packages
- [Releases](releases.md) - Releases created from packages
- [Libraries](libraries.md) - Library packages
- [Jobs](jobs.md) - Jobs executing packaged processes

## Methods

### get()
Get a list of packages with optional filters.

```python
packages = client.packages.get(
    is_active=True,           # Filter by active status
    is_latest=True,          # Filter for latest versions
    package_key="MyPackage"  # Filter by package key
)
```

#### Parameters
- `is_active` (bool, optional): Filter by active status
- `is_latest` (bool, optional): Filter for latest versions only
- `package_key` (str, optional): Filter by package key

#### Returns
List[Dict]: List of package objects matching the filters

### get_by_id()
Get a specific package by ID.

```python
package = client.packages.get_by_id(123)
```

#### Parameters
- `package_id` (int): ID of the package to retrieve

#### Returns
Dict: Package details

### get_by_key()
Get a package by its key.

```python
package = client.packages.get_by_key("package-key-123")
```

#### Parameters
- `key` (str): Package key

#### Returns
Dict: Package details

### upload()
Upload a new package (.nupkg file).

```python
package = client.packages.upload(
    file_path="MyProcess.1.0.0.nupkg",
    version="1.0.0"  # Optional
)
```

#### Parameters
- `file_path` (str): Path to the .nupkg file
- `version` (str, optional): Version string

#### Returns
Dict: Uploaded package details

### upload_stream()
Upload a package from a file stream.

```python
with open("MyProcess.nupkg", "rb") as f:
    package = client.packages.upload_stream(
        file_stream=f,
        filename="MyProcess.nupkg"
    )
```

#### Parameters
- `file_stream` (BinaryIO): File-like object containing the package
- `filename` (str): Name of the file

#### Returns
Dict: Uploaded package details

### download()
Download a package.

```python
content = client.packages.download(123)
with open("MyProcess.nupkg", "wb") as f:
    f.write(content)
```

#### Parameters
- `package_id` (int): ID of the package to download

#### Returns
bytes: The package content

### delete()
Delete a package.

```python
client.packages.delete(123)
```

#### Parameters
- `package_id` (int): ID of package to delete

### set_active()
Set the active status of a package.

```python
client.packages.set_active(123, True)
```

#### Parameters
- `package_id` (int): ID of the package
- `is_active` (bool): Whether the package should be active

## Examples

### Package Management

```python
def manage_package_versions(package_key: str, keep_versions: int = 3):
    """Manage package versions, keeping only the most recent ones"""
    # Get all versions
    packages = client.packages.get(package_key=package_key)
    
    # Sort by version
    packages.sort(key=lambda x: x["Version"], reverse=True)
    
    # Keep latest versions
    to_delete = packages[keep_versions:]
    
    results = {
        "kept": [p["Version"] for p in packages[:keep_versions]],
        "deleted": []
    }
    
    # Delete old versions
    for package in to_delete:
        try:
            # Download for archival
            content = client.packages.download(package["Id"])
            archive_path = f"archive/{package_key}_{package['Version']}.nupkg"
            
            with open(archive_path, "wb") as f:
                f.write(content)
            
            # Delete from Orchestrator
            client.packages.delete(package["Id"])
            
            results["deleted"].append({
                "version": package["Version"],
                "archived": True
            })
            
        except Exception as e:
            results["deleted"].append({
                "version": package["Version"],
                "error": str(e)
            })
    
    return results

# Manage package versions
results = manage_package_versions("MyProcess", keep_versions=3)
```

### Package Deployment

```python
def deploy_package(file_path: str, environment_id: int):
    """Deploy a package to a specific environment"""
    try:
        # Upload package
        package = client.packages.upload(file_path)
        
        # Create release
        release = client.releases.create({
            "Name": f"Release_{package['Version']}",
            "ProcessKey": package["Key"],
            "ProcessVersion": package["Version"],
            "EnvironmentId": environment_id
        })
        
        return {
            "package": package,
            "release": release,
            "status": "deployed"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Deploy package
result = deploy_package(
    "MyProcess.1.0.0.nupkg",
    environment_id=123
)
```

### Package Validation

```python
def validate_package(file_path: str):
    """Validate package before deployment"""
    import zipfile
    import json
    
    validations = {
        "file_exists": False,
        "valid_nupkg": False,
        "has_project_json": False,
        "has_main_xaml": False
    }
    
    try:
        # Check file exists
        validations["file_exists"] = os.path.exists(file_path)
        
        # Check valid nupkg
        with zipfile.ZipFile(file_path) as z:
            # Check project.json
            if "project.json" in z.namelist():
                validations["has_project_json"] = True
                
                # Parse project.json
                with z.open("project.json") as f:
                    project = json.load(f)
                    main_file = project.get("main", "Main.xaml")
                    
                    # Check main workflow exists
                    validations["has_main_xaml"] = main_file in z.namelist()
            
            validations["valid_nupkg"] = True
            
    except zipfile.BadZipFile:
        validations["valid_nupkg"] = False
    except Exception as e:
        validations["error"] = str(e)
    
    return validations

# Validate package
validation_results = validate_package("MyProcess.nupkg")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to upload invalid package
    client.packages.upload("invalid.nupkg")
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid package format")
    elif e.response.status_code == 409:
        print("Package version conflict")
    else:
        print(f"Error uploading package: {e}")
```

## Best Practices

1. Use semantic versioning
2. Validate packages before upload
3. Archive old versions
4. Document package contents
5. Test in development first
6. Maintain version history
7. Regular cleanup of old versions
8. Monitor package usage
9. Secure package storage

## Security Considerations

1. Control package access
2. Validate package sources
3. Scan for security issues
4. Monitor package usage
5. Secure package storage
6. Audit package changes
7. Version control integration

## See Also
- [UiPath Packages Documentation](https://docs.uipath.com/orchestrator/docs/about-packages)
- [Package Management](https://docs.uipath.com/orchestrator/docs/managing-packages)
- [Package Security](https://docs.uipath.com/orchestrator/docs/package-security)
- [Processes](processes.md) for process management
- [Releases](releases.md) for release management 
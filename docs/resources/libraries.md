# Libraries

The Libraries resource allows you to manage UiPath libraries (packages) in Orchestrator. Libraries are reusable components that can be shared across multiple automation projects.

## Related Resources
- [Processes](processes.md) - Processes that use libraries
- [Packages](packages.md) - Similar package management
- [Releases](releases.md) - Releases that depend on libraries

## Methods

### get()
Get a list of libraries with optional filters.

```python
libraries = client.libraries.get(
    version="1.0.0",          # Filter by version
    title="MyLibrary",       # Filter by package title
    is_latest=True          # Filter for latest versions
)
```

#### Parameters
- `version` (str, optional): Filter by version
- `title` (str, optional): Filter by package title
- `is_latest` (bool, optional): Filter for latest versions only

#### Returns
List[Dict]: List of library objects matching the filters

### get_by_id()
Get a specific library by ID.

```python
library = client.libraries.get_by_id(123)
```

#### Parameters
- `library_id` (int): ID of the library to retrieve

#### Returns
Dict: Library details

### upload()
Upload a new library package (.nupkg file).

```python
library = client.libraries.upload("MyLibrary.1.0.0.nupkg")
```

#### Parameters
- `file_path` (str): Path to the .nupkg file

#### Returns
Dict: Uploaded library details

### upload_stream()
Upload a library from a file stream.

```python
with open("MyLibrary.nupkg", "rb") as f:
    library = client.libraries.upload_stream(
        file_stream=f,
        filename="MyLibrary.nupkg"
    )
```

#### Parameters
- `file_stream` (BinaryIO): File-like object containing the library package
- `filename` (str): Name of the file

#### Returns
Dict: Uploaded library details

### download()
Download a library package.

```python
content = client.libraries.download(123)
with open("MyLibrary.nupkg", "wb") as f:
    f.write(content)
```

#### Parameters
- `library_id` (int): ID of the library to download

#### Returns
bytes: The library package content

### delete()
Delete a library.

```python
client.libraries.delete(123)
```

#### Parameters
- `library_id` (int): ID of library to delete

### delete_version()
Delete a specific version of a library.

```python
client.libraries.delete_version(123, "1.0.0")
```

#### Parameters
- `library_id` (int): ID of the library
- `version` (str): Version string to delete

### get_versions()
Get all versions of a specific library.

```python
versions = client.libraries.get_versions("MyLibrary")
```

#### Parameters
- `title` (str): The library title to get versions for

#### Returns
List[Dict]: List of library versions

### get_dependencies()
Get dependencies for a specific library.

```python
dependencies = client.libraries.get_dependencies(123)
```

#### Parameters
- `library_id` (int): ID of the library

#### Returns
List[Dict]: Library dependencies

## Examples

### Library Management

```python
# Upload new library version
library = client.libraries.upload("MyLibrary.1.0.0.nupkg")

# Check dependencies
dependencies = client.libraries.get_dependencies(library["Id"])

# Get all versions
versions = client.libraries.get_versions(library["Title"])

# Clean up old versions
for version in versions:
    if version["Version"].startswith("0."):
        client.libraries.delete_version(
            version["Id"],
            version["Version"]
        )
```

### Library Deployment

```python
def deploy_library(file_path: str):
    # Upload library
    library = client.libraries.upload(file_path)
    
    # Verify dependencies
    dependencies = client.libraries.get_dependencies(library["Id"])
    
    # Check if all dependencies are available
    for dep in dependencies:
        try:
            versions = client.libraries.get_versions(dep["Title"])
            if not any(v["Version"] == dep["Version"] for v in versions):
                print(f"Missing dependency: {dep['Title']} {dep['Version']}")
        except Exception as e:
            print(f"Error checking dependency {dep['Title']}: {e}")
    
    return library

# Deploy library
new_library = deploy_library("MyLibrary.1.0.0.nupkg")
```

### Version Management

```python
def manage_library_versions(title: str, keep_versions: int = 3):
    # Get all versions
    versions = client.libraries.get_versions(title)
    versions.sort(key=lambda x: x["Version"], reverse=True)
    
    # Keep latest versions
    versions_to_delete = versions[keep_versions:]
    
    for version in versions_to_delete:
        # Download for archival
        content = client.libraries.download(version["Id"])
        archive_path = f"archive/{title}_{version['Version']}.nupkg"
        
        # Save to archive
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        with open(archive_path, "wb") as f:
            f.write(content)
        
        # Delete from Orchestrator
        client.libraries.delete_version(version["Id"], version["Version"])

# Manage versions
manage_library_versions("MyLibrary", keep_versions=3)
```

### Bulk Operations

```python
def upload_directory(directory: str):
    """Upload all .nupkg files in a directory"""
    results = []
    
    for file in os.listdir(directory):
        if file.endswith(".nupkg"):
            try:
                library = client.libraries.upload(
                    os.path.join(directory, file)
                )
                results.append({
                    "file": file,
                    "status": "success",
                    "library": library
                })
            except Exception as e:
                results.append({
                    "file": file,
                    "status": "error",
                    "error": str(e)
                })
    
    return results

# Upload all libraries in directory
results = upload_directory("./libraries")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to upload invalid package
    client.libraries.upload("invalid.nupkg")
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid package format")
    elif e.response.status_code == 409:
        print("Package version conflict")
    else:
        print(f"Error uploading package: {e}")
```

## Best Practices

1. Use semantic versioning for libraries
2. Document library dependencies
3. Test libraries before deployment
4. Archive old versions before deletion
5. Maintain changelog for versions
6. Use consistent naming conventions
7. Keep dependencies up to date
8. Regular cleanup of unused versions
9. Document library usage and examples

## Security Considerations

1. Control access to library management
2. Validate package sources
3. Scan libraries for security issues
4. Monitor library usage
5. Audit library changes
6. Secure library storage
7. Review dependencies regularly

## See Also
- [UiPath Libraries Documentation](https://docs.uipath.com/orchestrator/docs/about-libraries)
- [Package Management](https://docs.uipath.com/orchestrator/docs/managing-packages)
- [Library Security](https://docs.uipath.com/orchestrator/docs/library-security)
- [Processes](processes.md) for using libraries
- [Packages](packages.md) for package management 
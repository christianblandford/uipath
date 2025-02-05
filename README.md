# UiPath Python SDK

A Python SDK for interacting with UiPath's APIs. This SDK provides a simple and intuitive way to automate UiPath operations programmatically.

## Installation 

```bash
pip install uipath
```

## Quick Start

```python
from uipath.auth.authentication import UiPathAuth
from uipath.client.api_client import UiPathClient
from uipath.resources.robots import RobotsResource

# Initialize authentication
auth = UiPathAuth(
    tenant_name="your_tenant",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Create API client
uipath = UiPathClient(auth)

```

## Features

- Complete API coverage for UiPath Orchestrator
- Simple, intuitive interface
- Authentication handling
- Comprehensive error handling
- Type hints for better IDE support
- Resource classes for all major UiPath entities:
  - Assets
  - Queues
  - Jobs
  - Folders
  - Releases
  - Packages
  - Libraries
  - Machines
  - Processes
  - Robots

## Authentication

The SDK supports OAuth2 client credentials authentication. You'll need:
- Client ID
- Client Secret
- Tenant name (optional)
- Organization ID (optional)

You can obtain these credentials from your UiPath Orchestrator account under Admin → API Access.

```python
auth = UiPathAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tenant_name="your_tenant",  # Optional
    organization_id="your_org_id",  # Optional
    scope="OR.Assets",  # Optional
    auth_url="https://cloud.uipath.com/identity_/connect/token"  # Optional
)

uipath = UiPathClient(auth)
```

## Usage Examples

### Working with Robots

```python
# List all robots
all_robots = uipath.robots.get()

# Get a specific robot
robot = uipath.robots.get_by_id(robot_id=123)

# Create a new robot
new_robot = uipath.robots.create({
    "Name": "MyNewRobot",
    "MachineId": 456,
    "Type": "Unattended",
    "Username": "domain\\user"
    })

# Update robot status
client.robots.toggle_enabled(robot_id=123, enabled=True)
```

### Working with Assets

```python
# List all assets
all_assets = uipath.assets.get()

# Get a specific asset
asset = uipath.assets.get_by_id(asset_id=123)

# Create a new asset
new_asset = uipath.assets.create({
    "Name": "DatabaseConnection",
    "ValueType": "Text",
    "Value": "connection_string",
    "CanBeDeleted": True
})

# Update an asset
uipath.assets.update(asset_id=123, value="new_connection_string")
```

### Working with Queues

```python
# List all queues
all_queues = uipath.queues.get()

# Add items to queue
queue_item = uipath.queues.add_queue_item(
    queue_name="InvoiceProcessing",
    reference="INV-001",
    priority="High",
    specific_content={
        "InvoiceNumber": "INV-001",
        "Amount": 1000.00,
        "DueDate": "2024-03-31"
    }
)

# Get queue items
items = uipath.queues.get_queue_items(
    queue_name="InvoiceProcessing",
    status="New"
)

# Set item status
uipath.queues.set_transaction_status(
    transaction_id=456,
    status="Successful"
)
```

### Working with Processes

```python
# List all processes
all_processes = uipath.processes.get()

# Get process details
process = uipath.processes.get_by_id(process_id=123)

# Start a process
uipath.processes.start({
    "releaseKey": "process-release-key",
    "strategy": "ModernJobsCount",
    "jobsCount": 1,
    "inputArguments": {
        "param1": "value1"
    }
})
```

### Working with Folders

```python
# List all folders
all_folders = uipath.folders.get()

# Create a new folder
new_folder = uipath.folders.create({
    "DisplayName": "Finance Department",
    "Description": "Automation processes for finance",
    "ProvisionType": "Manual"
})

# Get folder details
folder = uipath.folders.get_by_id(folder_id=123)

# Update folder permissions
uipath.folders.set_permissions(
    folder_id=123,
    permissions=["View", "Edit", "Create", "Delete"]
)
```

### Working with Packages

```python
# List all packages
all_packages = uipath.packages.get()

# Upload a new package
with open("MyProcess.nupkg", "rb") as package:
    new_package = uipath.packages.upload(package)

# Delete a package
uipath.packages.delete(package_id=123)

# Get package versions
versions = uipath.packages.get_versions(package_name="MyProcess")
```

### Working with Libraries

```python
# List all libraries
all_libraries = uipath.libraries.get()

# Get library details
library = uipath.libraries.get_by_id(library_id=123)

# Add library to process
uipath.libraries.add_to_process(
    process_id=456,
    library_id=123
)
```

### Working with Machines

```python
# List all machines
all_machines = uipath.machines.get()

# Register a new machine
new_machine = uipath.machines.create({
    "Name": "RPA-MACHINE-01",
    "Description": "Finance department RPA machine",
    "Type": "Standard"
})

# Update machine status
uipath.machines.update_status(
    machine_id=123,
    status="Available"
)
```

### Error Handling

The SDK provides custom exceptions for different types of errors:

```python
from uipath.exceptions.exceptions import AuthenticationError, ApiError

try:
    robots.get_robot(robot_id=999)
except AuthenticationError as e:
    print("Authentication failed:", e)
except ApiError as e:
    print("API request failed:", e)
```

## Configuration

The SDK can be configured with custom endpoints and API versions:

```python
client = UiPathClient(
    auth,
    base_url="https://cloud.uipath.com",  # Custom base URL
    api_version="v1"  # API version
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions, please:
1. Check the [documentation](docs/)
2. Open an issue in the GitHub repository

## Requirements

- Python 3.7+
- requests library

## Disclaimer

This is an unofficial SDK and is not affiliated with, maintained, authorized, endorsed, or sponsored by UiPath.

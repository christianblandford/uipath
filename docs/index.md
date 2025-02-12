# UiPath Python SDK

A Python SDK for interacting with the UiPath Orchestrator API.

## Features

- Complete API coverage for UiPath Orchestrator
- Easy-to-use interface
- Type hints for better IDE support
- Comprehensive documentation
- Examples for common use cases

## Installation 

```bash
pip install uipath
```


## Quick Start

```python
from uipath import UiPathClient

client = UiPathClient(
    organization_id="your_organization_id",
    tenant_id="your_tenant_id",
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

## Resource Examples

### Assets

```python
# Get all assets
assets = client.assets.get()

# Create an asset
asset = client.assets.create({
    "Name": "DatabaseConnection",
    "ValueType": "Text",
    "Value": "connection_string_here"
})

# Get asset by name
asset = client.assets.get_by_name("DatabaseConnection")

# Update asset
client.assets.update(asset["Id"], {
    "Value": "new_connection_string"
})
```

### Directory Service

```python
# Get available domains
domains = client.directory.get_domains()

# Search for users and groups
users = client.directory.search_users_and_groups(
    search_context="Users",
    domain="mydomain",
    prefix="john"
)

# Get directory permissions
permissions = client.directory.get_permissions(
    username="john.doe",
    domain="mydomain"
)
```

### Folders

```python
# Get all folders
folders = client.folders.get()

# Get folder by ID
folder = client.folders.get_by_id(123)

# Get folder hierarchy
hierarchy = client.folders.get_folder_hierarchy()

# Update folder
client.folders.update_name_description(
    key="folder_key",
    name="New Name",
    description="New description"
)
```

### Jobs

```python
# Get jobs
jobs = client.jobs.get(
    state="Successful",
    robot_name="MyRobot"
)

# Start job
job = client.jobs.start_jobs({
    "startInfo": {
        "ReleaseKey": "release_key",
        "Strategy": "Specific",
        "RobotIds": [123, 456]
    }
})

# Stop job
client.jobs.stop_job(job["Id"])
```

### Libraries

```python
# Get all libraries
libraries = client.libraries.get()

# Create library
library = client.libraries.create({
    "Name": "MyLibrary",
    "Version": "1.0.0"
})

# Delete library
client.libraries.delete(library["Id"])
```

### Licensing

```python
# Acquire license units
result = client.licensing.acquire({
    "count": 5,
    "licenseType": "Unattended"
})

# Release license units
client.licensing.release({
    "count": 2,
    "licenseType": "Unattended"
})
```

### Logs

```python
# Submit multiple log entries
client.logs.submit_logs([
    {
        "message": "Process started",
        "level": "Information",
        "timeStamp": "2023-01-18T14:46:07.4152893+02:00",
        "processName": "MyProcess"
    }
])
```

### Machines

```python
# Get all machines
machines = client.machines.get()

# Get machine by name
machine = client.machines.get_by_name("MyMachine")

# Update machine
client.machines.update(machine["Id"], {
    "Name": "NewMachineName",
    "Description": "Updated description"
})
```

### Maintenance

```python
# Start maintenance window
client.maintenance.start(
    phase="Draining",
    force=False,
    kill_jobs=False
)

# End maintenance
client.maintenance.end()
```

### Packages

```python
# Get all packages
packages = client.packages.get()

# Upload package
with open("MyPackage.nupkg", "rb") as f:
    package = client.packages.upload(f)

# Delete package
client.packages.delete(package["Id"])
```

### Processes

```python
# Get all processes
processes = client.processes.get()

# Get process by ID
process = client.processes.get_by_id(123)

# Start process
client.processes.start_process(
    process_id=123,
    robot_ids=[456],
    input_arguments={"param1": "value1"}
)
```

### Queues

```python
# Get all queues
queues = client.queues.get()

# Add queue item
client.queues.add_queue_item(
    queue_name="MyQueue",
    item_data={"field1": "value1"}
)

# Get queue items
items = client.queues.get_queue_items(
    queue_name="MyQueue",
    status="New"
)
```

### Releases

```python
# Get all releases
releases = client.releases.get()

# Create release
release = client.releases.create({
    "Name": "MyRelease",
    "ProcessKey": "process_key",
    "EnvironmentId": 123
})

# Delete release
client.releases.delete(release["Id"])
```

### Robots

```python
# Get all robots
robots = client.robots.get()

# Get robot by name
robot = client.robots.get_by_name("MyRobot")

# Update robot
client.robots.update(robot["Id"], {
    "Name": "NewRobotName",
    "Description": "Updated description"
})

# Toggle robot enabled state
client.robots.toggle_enabled(robot["Id"], enabled=True)
```

### Stats

```python
# Get job statistics
job_stats = client.stats.get_jobs_stats()

# Get license usage
license_stats = client.stats.get_license_stats(days=30)

# Get session stats
session_stats = client.stats.get_sessions_stats()
```

### Status

```python
# Check service status
status = client.status.get()

# Verify host availability
result = client.status.verify_host_availability("https://myhost.com")
```

### Task Forms

```python
# Get tasks with filters
tasks = client.task_forms.get_tasks(
    title="Review Document",
    status="Pending",
    take=10
)

# Complete a task
client.task_forms.complete_task(
    task_id=123,
    action="Approved"
)
```

### Test Automation

```python
# Start test set execution
execution_id = client.test_automation.start_test_set_execution(
    test_set_id=456,
    trigger_type="Manual"
)

# Cancel test execution
client.test_automation.cancel_test_set_execution(test_set_execution_id=789)

# Get test case execution results
results = client.test_automation.get_package_info(
    test_case_unique_id="test_id",
    package_identifier="package_id"
)
```

### Test Data Queue

```python
# Add queue item
client.test_data_queue.add_item(
    queue_name="TestQueue",
    content={"data": "test value"}
)

# Bulk add items
items = [
    {"data": "value1"},
    {"data": "value2"}
]
client.test_data_queue.bulk_add_items("TestQueue", items)

# Delete all items
client.test_data_queue.delete_all_items("TestQueue")
```

### Webhooks

```python
# Create webhook
webhook = client.webhooks.create({
    "Name": "MyWebhook",
    "Url": "https://my-webhook-handler.com",
    "Enabled": True,
    "SubscribeToAllEvents": False,
    "AllowInsecureSsl": False,
    "Events": [
        {"EventType": "Job.Completed"},
        {"EventType": "Job.Faulted"}
    ]
})

# Get webhook event types
event_types = client.webhooks.get_event_types()

# Test webhook
client.webhooks.ping(webhook["Id"])
```

## Additional Resources

For more detailed information about specific resources and their methods, please refer to the API documentation or the source code docstrings.

## Error Handling

The SDK will raise appropriate exceptions when API calls fail. It's recommended to handle these exceptions in your code:

```python
from requests.exceptions import HTTPError

try:
    client.robots.get_by_name("NonExistentRobot")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Robot not found")
    else:
        print(f"API error: {e}")
```

## Authentication

The SDK supports different authentication methods:

```python
# Using client credentials
client = UiPathClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    organization_id="your_org_id",
    tenant_id="your_tenant_id"
)

# Using username/password
client = UiPathClient(
    username="your_username",
    password="your_password",
    organization_id="your_org_id",
    tenant_id="your_tenant_id"
)
```
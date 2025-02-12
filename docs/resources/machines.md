# Machines

The Machines resource allows you to manage UiPath Orchestrator machines. Machines are the physical or virtual computers where UiPath robots run automation processes.

## Related Resources
- [Robots](robots.md) - Robots that run on machines
- [Jobs](jobs.md) - Jobs that execute on machines
- [Releases](releases.md) - Releases that run on machines
- [Licensing](licensing.md) - Machine licensing information

## Methods

### get()
Get a list of machines with optional filters.

```python
machines = client.machines.get(
    name="DESKTOP-123",        # Filter by machine name
    type="Standard",          # Filter by machine type
    is_online=True           # Filter by online status
)
```

#### Parameters
- `name` (str, optional): Filter by machine name
- `type` (str, optional): Filter by machine type (Standard, Template)
- `is_online` (bool, optional): Filter by online status

#### Returns
List[Dict]: List of machine objects matching the filters

### get_by_id()
Get a specific machine by ID.

```python
machine = client.machines.get_by_id(123)
```

#### Parameters
- `machine_id` (int): ID of the machine to retrieve

#### Returns
Dict: Machine details

### get_by_key()
Get a machine by its license key.

```python
machine = client.machines.get_by_key("license-key-123")
```

#### Parameters
- `key` (str): Machine license key

#### Returns
Dict: Machine details

### create()
Create a new machine.

```python
machine = client.machines.create({
    "Name": "DESKTOP-123",
    "Type": "Standard",
    "NonProductionSlots": 2,
    "UnattendedSlots": 3,
    "Description": "Development machine"
})
```

#### Parameters
- `machine_data` (Dict): Machine configuration including:
  - `Name` (str, required): Machine name
  - `Type` (str, required): Machine type
  - `NonProductionSlots` (int, optional): Number of non-production slots
  - `UnattendedSlots` (int, optional): Number of unattended slots
  - `Description` (str, optional): Machine description

#### Returns
Dict: Created machine details

### update()
Update an existing machine.

```python
client.machines.update(123, {
    "Description": "Updated description",
    "NonProductionSlots": 3
})
```

#### Parameters
- `machine_id` (int): ID of machine to update
- `machine_data` (Dict): Updated machine data

#### Returns
Dict: Updated machine details

### delete()
Delete a machine.

```python
client.machines.delete(123)
```

#### Parameters
- `machine_id` (int): ID of machine to delete

### get_license_info()
Get license information for a machine.

```python
license_info = client.machines.get_license_info(123)
```

#### Parameters
- `machine_id` (int): ID of the machine

#### Returns
Dict: Machine license information

### get_machine_settings()
Get settings for a specific machine.

```python
settings = client.machines.get_machine_settings(123)
```

#### Parameters
- `machine_id` (int): ID of the machine

#### Returns
Dict: Machine settings

### update_machine_settings()
Update settings for a specific machine.

```python
client.machines.update_machine_settings(123, {
    "TracingLevel": "Error",
    "LogLevel": "Info",
    "ExecutionConcurrency": 3
})
```

#### Parameters
- `machine_id` (int): ID of the machine
- `settings` (Dict): Updated settings

### get_robots()
Get all robots associated with a machine.

```python
robots = client.machines.get_robots(123)
```

#### Parameters
- `machine_id` (int): ID of the machine

#### Returns
List[Dict]: List of robots on the machine

### delete_by_key()
Delete a machine by its license key.

```python
client.machines.delete_by_key("license-key-123")
```

#### Parameters
- `key` (str): Machine license key

## Examples

### Machine Provisioning

```python
def provision_machine(name: str, robot_slots: int):
    # Create machine
    machine = client.machines.create({
        "Name": name,
        "Type": "Standard",
        "UnattendedSlots": robot_slots,
        "Description": f"Provisioned on {datetime.now()}"
    })
    
    # Configure machine settings
    client.machines.update_machine_settings(
        machine["Id"],
        {
            "TracingLevel": "Error",
            "LogLevel": "Info",
            "ExecutionConcurrency": robot_slots
        }
    )
    
    return machine

# Provision development machine
dev_machine = provision_machine("DEV-MACHINE-001", 2)
```

### Machine Maintenance

```python
def check_machine_health(machine_id: int):
    # Get machine details
    machine = client.machines.get_by_id(machine_id)
    
    # Check license status
    license_info = client.machines.get_license_info(machine_id)
    
    # Get connected robots
    robots = client.machines.get_robots(machine_id)
    
    return {
        "is_online": machine.get("IsOnline", False),
        "license_valid": license_info.get("IsValid", False),
        "connected_robots": len(robots),
        "last_seen": machine.get("LastModificationTime")
    }

# Monitor machine health
health_status = check_machine_health(123)
```

### Machine Cleanup

```python
def cleanup_offline_machines(days_threshold: int = 30):
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days_threshold)
    
    # Get all machines
    machines = client.machines.get()
    
    for machine in machines:
        last_seen = datetime.fromisoformat(machine["LastModificationTime"])
        if not machine["IsOnline"] and last_seen < cutoff_date:
            # Archive machine data if needed
            print(f"Archiving machine {machine['Name']}")
            
            # Delete machine
            client.machines.delete(machine["Id"])

# Clean up inactive machines
cleanup_offline_machines(30)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create machine with duplicate name
    client.machines.create({
        "Name": "ExistingMachine",
        "Type": "Standard"
    })
except HTTPError as e:
    if e.response.status_code == 409:
        print("Machine with this name already exists")
    elif e.response.status_code == 400:
        print("Invalid machine configuration")
    else:
        print(f"Error creating machine: {e}")
```

## Best Practices

1. Use consistent naming conventions for machines
2. Monitor machine health regularly
3. Keep machine settings optimized for workload
4. Clean up unused machines
5. Document machine configurations
6. Maintain appropriate robot slot allocations
7. Regular license validation
8. Monitor machine resource usage
9. Keep machines updated

## Security Considerations

1. Control machine access permissions
2. Secure machine credentials
3. Monitor machine activities
4. Regular security updates
5. Network security configuration
6. Audit machine changes
7. License compliance

## See Also
- [UiPath Machines Documentation](https://docs.uipath.com/orchestrator/docs/about-machines)
- [Machine Management](https://docs.uipath.com/orchestrator/docs/managing-machines)
- [Machine Security](https://docs.uipath.com/orchestrator/docs/machine-security)
- [Robots](robots.md) for robot management
- [Licensing](licensing.md) for license management 
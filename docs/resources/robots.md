# Robots

The Robots resource allows you to manage UiPath robots in your organization.

## Related Resources
- [Machines](machines.md) - Manage machines where robots run
- [Jobs](jobs.md) - Execute and monitor robot jobs
- [Releases](releases.md) - Manage process releases that robots can execute

## Methods

### get()
Get a list of robots with optional filters.

```python
robots = client.robots.get(
    name="MyRobot",           # Filter by robot name
    machine_id=123,           # Filter by machine ID
    type="Unattended",        # Filter by robot type
    is_connected=True,        # Filter by connection status
    user_id=456              # Filter by associated user ID
)
```

#### Parameters
- `name` (str, optional): Filter by robot name
- `machine_id` (int, optional): Filter by machine ID
- `type` (str, optional): Filter by robot type. Valid values:
  - `Unattended`
  - `Attended`
  - `NonProduction`
  - `TestAutomation`
- `is_connected` (bool, optional): Filter by connection status
- `user_id` (int, optional): Filter by associated user ID

#### Returns
List[Dict]: List of robot objects matching the filters

### get_by_id()
Get a specific robot by ID.

```python
robot = client.robots.get_by_id(123)
```

#### Parameters
- `robot_id` (int): ID of the robot to retrieve

#### Returns
Dict: Robot details

### create()
Create a new robot.

```python
robot = client.robots.create({
    "Name": "MyRobot",
    "MachineId": 123,
    "Type": "Unattended",
    "Username": "domain\\user",
    "Password": "password",  # Optional
    "Description": "My robot description"
})
```

#### Parameters
- `robot_data` (Dict): Robot configuration including:
  - `Name` (str, required): Robot name
  - `MachineId` (int, required): Associated machine ID
  - `Type` (str, required): Robot type
  - `Username` (str, required): Associated Windows username
  - `Password` (str, optional): Windows password
  - `Description` (str, optional): Robot description

#### Returns
Dict: Created robot details

### update()
Update an existing robot.

```python
client.robots.update(123, {
    "Name": "NewRobotName",
    "Description": "Updated description"
})
```

#### Parameters
- `robot_id` (int): ID of robot to update
- `robot_data` (Dict): Updated robot data

#### Returns
Dict: Updated robot details

### delete()
Delete a robot.

```python
client.robots.delete(123)
```

#### Parameters
- `robot_id` (int): ID of robot to delete

### get_license()
Get license information for a robot.

```python
license_info = client.robots.get_license(123)
```

#### Parameters
- `robot_id` (int): ID of the robot

#### Returns
Dict: Robot license information

### toggle_enabled()
Enable or disable a robot.

```python
client.robots.toggle_enabled(123, enabled=True)
```

#### Parameters
- `robot_id` (int): ID of the robot
- `enabled` (bool): Whether to enable or disable the robot

## Examples

### Creating and Configuring a Robot

```python
# Create a new robot
robot = client.robots.create({
    "Name": "ProcessingBot",
    "MachineId": 123,
    "Type": "Unattended",
    "Username": "domain\\processuser"
})

# Enable the robot
client.robots.toggle_enabled(robot["Id"], enabled=True)

# Update robot credentials
client.robots.update_user(
    robot["Id"], 
    {
        "Username": "domain\\newuser",
        "Password": "newpassword"
    }
)
```

### Managing Robot Status

```python
# Get robot status
status = client.robots.get_status(123)

# Get active sessions
sessions = client.robots.get_sessions(123)

# Get machine name
machine_name = client.robots.get_machine_name_by_id(123)
```

### Filtering Robots

```python
# Get all connected unattended robots
robots = client.robots.get(
    type="Unattended",
    is_connected=True
)

# Get robots on specific machine
robots = client.robots.get(machine_id=123)

# Get robots by name pattern
robots = client.robots.get(name="ProcessingBot*")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    robot = client.robots.get_by_id(999)
except HTTPError as e:
    if e.response.status_code == 404:
        print("Robot not found")
    else:
        print(f"Error managing robot: {e}")
```

## See Also
- [UiPath Robots Documentation](https://docs.uipath.com/orchestrator/docs/about-robots)
- [Robot Security](https://docs.uipath.com/orchestrator/docs/robot-security)
- [Managing Robot Credentials](https://docs.uipath.com/orchestrator/docs/managing-robot-credentials) 
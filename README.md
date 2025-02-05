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
client = UiPathClient(auth)

# Use the robots resource
robots = RobotsResource(client)

# List all robots
all_robots = robots.list_robots()
```

## Features

- Simple, intuitive interface for UiPath APIs
- Authentication handling
- Comprehensive error handling
- Type hints for better IDE support
- Resource classes for all major UiPath entities:
  - Robots
  - Jobs
  - Processes
  - Assets
  - And more...

## Authentication

The SDK supports client credentials authentication. You'll need:
- Tenant name
- Client ID
- Client secret

You can obtain these credentials from your UiPath Orchestrator account under Admin → API Access.

```python
auth = UiPathAuth(
    tenant_name="your_tenant",
    client_id="your_client_id",
    client_secret="your_client_secret",
    scope="OR.Default"  # Optional, defaults to OR.Default
)
```

## Usage Examples

### Working with Robots

```python
# List all robots
robots = RobotsResource(client)
all_robots = robots.list_robots()

# Get a specific robot
robot = robots.get_robot(robot_id=123)

# Create a new robot
new_robot = robots.create_robot(
    name="MyNewRobot",
    machine_name="DESKTOP-123",
    type="Unattended"
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

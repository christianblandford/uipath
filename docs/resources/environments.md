# Environments

The Environments resource allows you to manage UiPath Orchestrator environments, which are logical groupings of resources like robots, processes, and assets for different deployment stages or business units.

## Related Resources
- [Robots](robots.md) - Robots assigned to environments
- [Processes](processes.md) - Processes deployed to environments
- [Assets](assets.md) - Assets configured per environment
- [Releases](releases.md) - Releases deployed to environments

## Methods

### get()
Get a list of environments with optional filters.

```python
environments = client.environments.get(
    name="Production",          # Filter by name
    organization_unit_id=123    # Filter by organization unit
)
```

#### Parameters
- `name` (str, optional): Filter by environment name
- `organization_unit_id` (int, optional): Filter by organization unit ID

#### Returns
List[Dict]: List of environment objects matching the filters

### get_by_id()
Get a specific environment by ID.

```python
environment = client.environments.get_by_id(123)
```

#### Parameters
- `environment_id` (int): ID of the environment to retrieve

#### Returns
Dict: Environment details

### create()
Create a new environment.

```python
environment = client.environments.create({
    "Name": "Production",
    "Description": "Production environment",
    "Type": "Standard",
    "OrganizationUnitId": 123
})
```

#### Parameters
- `environment_data` (Dict): Environment configuration including:
  - `Name` (str, required): Environment name
  - `Description` (str, optional): Environment description
  - `Type` (str, optional): Environment type
  - `OrganizationUnitId` (int, optional): Organization unit ID

#### Returns
Dict: Created environment details

### update()
Update an existing environment.

```python
client.environments.update(123, {
    "Name": "Production-2023",
    "Description": "Updated production environment"
})
```

#### Parameters
- `environment_id` (int): ID of environment to update
- `environment_data` (Dict): Updated environment data

### delete()
Delete an environment.

```python
client.environments.delete(123)
```

#### Parameters
- `environment_id` (int): ID of environment to delete

## Examples

### Environment Setup

```python
def setup_deployment_environments():
    """Setup standard deployment environments"""
    environments = {
        "Development": {
            "Description": "Development and testing environment",
            "Type": "Development"
        },
        "Staging": {
            "Description": "Pre-production validation environment",
            "Type": "Staging"
        },
        "Production": {
            "Description": "Production environment",
            "Type": "Production"
        }
    }
    
    created_envs = {}
    for name, config in environments.items():
        try:
            env = client.environments.create({
                "Name": name,
                "Description": config["Description"],
                "Type": config["Type"]
            })
            created_envs[name] = env
            
        except Exception as e:
            print(f"Error creating environment {name}: {e}")
    
    return created_envs

# Setup environments
environments = setup_deployment_environments()
```

### Resource Assignment

```python
def assign_resources_to_environment(environment_id: int, resources: Dict):
    """Assign resources to an environment"""
    results = {
        "robots": [],
        "processes": [],
        "assets": []
    }
    
    # Assign robots
    for robot_id in resources.get("robot_ids", []):
        try:
            client.robots.update(robot_id, {
                "EnvironmentId": environment_id
            })
            results["robots"].append({
                "robot_id": robot_id,
                "status": "assigned"
            })
        except Exception as e:
            results["robots"].append({
                "robot_id": robot_id,
                "status": "error",
                "error": str(e)
            })
    
    # Assign processes
    for process in resources.get("processes", []):
        try:
            client.processes.deploy({
                "ProcessKey": process["key"],
                "EnvironmentId": environment_id
            })
            results["processes"].append({
                "process": process["key"],
                "status": "deployed"
            })
        except Exception as e:
            results["processes"].append({
                "process": process["key"],
                "status": "error",
                "error": str(e)
            })
    
    return results

# Assign resources
resources = {
    "robot_ids": [123, 456],
    "processes": [
        {"key": "InvoiceProcess"},
        {"key": "PayrollProcess"}
    ]
}
assignments = assign_resources_to_environment(789, resources)
```

### Environment Promotion

```python
def promote_to_production(staging_env_id: int, prod_env_id: int):
    """Promote resources from staging to production"""
    # Get staging resources
    staging_robots = client.robots.get(environment_id=staging_env_id)
    staging_processes = client.processes.get(environment_id=staging_env_id)
    
    # Promote each resource
    promotions = {
        "robots": [],
        "processes": [],
        "status": "in_progress"
    }
    
    try:
        # Promote robots
        for robot in staging_robots:
            prod_robot = client.robots.create({
                "Name": f"PROD_{robot['Name']}",
                "Type": robot["Type"],
                "EnvironmentId": prod_env_id
            })
            promotions["robots"].append({
                "staging_id": robot["Id"],
                "production_id": prod_robot["Id"]
            })
        
        # Promote processes
        for process in staging_processes:
            prod_process = client.processes.deploy({
                "ProcessKey": process["Key"],
                "EnvironmentId": prod_env_id,
                "Version": process["Version"]
            })
            promotions["processes"].append({
                "key": process["Key"],
                "status": "promoted"
            })
        
        promotions["status"] = "completed"
        
    except Exception as e:
        promotions["status"] = "error"
        promotions["error"] = str(e)
    
    return promotions

# Promote to production
promotion_results = promote_to_production(
    staging_env_id=456,
    prod_env_id=789
)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create environment with duplicate name
    client.environments.create({
        "Name": "ExistingEnvironment",
        "Type": "Production"
    })
except HTTPError as e:
    if e.response.status_code == 409:
        print("Environment with this name already exists")
    elif e.response.status_code == 400:
        print("Invalid environment configuration")
    else:
        print(f"Error creating environment: {e}")
```

## Best Practices

1. Use consistent naming conventions
2. Maintain clear environment separation
3. Document environment purposes
4. Control access per environment
5. Regular environment cleanup
6. Test promotion processes
7. Monitor environment usage
8. Backup environment configs
9. Version control configurations

## Security Considerations

1. Restrict environment access
2. Separate production access
3. Audit environment changes
4. Secure configuration data
5. Monitor resource usage
6. Control promotion process
7. Regular security reviews

## See Also
- [UiPath Environments Documentation](https://docs.uipath.com/orchestrator/docs/about-environments)
- [Environment Management](https://docs.uipath.com/orchestrator/docs/managing-environments)
- [Environment Security](https://docs.uipath.com/orchestrator/docs/environment-security)
- [Robots](robots.md) for robot management
- [Processes](processes.md) for process deployment 
# Assets

The Assets resource allows you to manage UiPath Orchestrator assets. Assets are used to store and manage configuration values, credentials, and other settings that can be used across different processes.

## Related Resources
- [Robots](robots.md) - Robots can use assets during execution
- [Processes](processes.md) - Processes can reference assets
- [Jobs](jobs.md) - Jobs can use assets during execution

## Methods

### get()
Get a list of assets with optional filters.

```python
assets = client.assets.get(
    name="DatabaseConnection",    # Filter by asset name
    folder_id=123                # Filter by folder ID
)
```

#### Parameters
- `name` (str, optional): Filter by asset name
- `folder_id` (int, optional): Filter by folder ID

#### Returns
List[Dict]: List of asset objects matching the filters

### get_by_id()
Get a specific asset by ID.

```python
asset = client.assets.get_by_id(123)
```

#### Parameters
- `asset_id` (int): ID of the asset to retrieve

#### Returns
Dict: Asset details

### get_by_name()
Get a specific asset by name.

```python
asset = client.assets.get_by_name("DatabaseConnection")
```

#### Parameters
- `name` (str): Name of the asset to retrieve

#### Returns
Dict: Asset details

### create()
Create a new asset.

```python
asset = client.assets.create({
    "Name": "DatabaseConnection",
    "ValueType": "Text",
    "Value": "Server=myserver;Database=mydb;",
    "Description": "Production database connection string",
    "CanBeDeleted": True,
    "ValueScope": "Global"
})
```

#### Parameters
- `asset_data` (Dict): Asset configuration including:
  - `Name` (str, required): Asset name
  - `ValueType` (str, required): Type of value. Valid values:
    - `Text`
    - `Integer`
    - `Boolean`
    - `Credential`
    - `WindowsCredential`
  - `Value` (Any, required): Asset value
  - `Description` (str, optional): Asset description
  - `CanBeDeleted` (bool, optional): Whether asset can be deleted
  - `ValueScope` (str, optional): Scope of the asset (Global, PerRobot)

#### Returns
Dict: Created asset details

### update()
Update an existing asset.

```python
client.assets.update(123, {
    "Value": "Server=newserver;Database=mydb;",
    "Description": "Updated connection string"
})
```

#### Parameters
- `asset_id` (int): ID of asset to update
- `asset_data` (Dict): Updated asset data

#### Returns
Dict: Updated asset details

### delete()
Delete an asset.

```python
client.assets.delete(123)
```

#### Parameters
- `asset_id` (int): ID of asset to delete

## Examples

### Managing Text Assets

```python
# Create a text asset
config_asset = client.assets.create({
    "Name": "ApiEndpoint",
    "ValueType": "Text",
    "Value": "https://api.example.com/v1",
    "Description": "API endpoint for production",
    "ValueScope": "Global"
})

# Update the endpoint
client.assets.update(config_asset["Id"], {
    "Value": "https://api.example.com/v2"
})
```

### Managing Credentials

```python
# Create a credential asset
cred_asset = client.assets.create({
    "Name": "ApiCredentials",
    "ValueType": "Credential",
    "Value": {
        "Username": "api_user",
        "Password": "api_password"
    },
    "Description": "API authentication credentials",
    "ValueScope": "Global"
})

# Create Windows credentials
win_cred = client.assets.create({
    "Name": "WindowsAuth",
    "ValueType": "WindowsCredential",
    "Value": {
        "Username": "domain\\user",
        "Password": "password"
    },
    "Description": "Windows authentication for network resources"
})
```

### Robot-Specific Assets

```python
# Create per-robot configuration
robot_config = client.assets.create({
    "Name": "ProcessingConfig",
    "ValueType": "Text",
    "Value": "default_config",
    "ValueScope": "PerRobot",
    "Description": "Robot-specific processing configuration"
})

# Set robot-specific value
client.assets.set_robot_asset_value(
    asset_id=robot_config["Id"],
    robot_id=456,
    value="custom_config"
)
```

### Managing Multiple Assets

```python
# Create multiple related assets
def create_environment_assets(env_name: str, config: dict):
    assets = []
    for key, value in config.items():
        asset = client.assets.create({
            "Name": f"{env_name}_{key}",
            "ValueType": "Text",
            "Value": value,
            "Description": f"{key} for {env_name} environment"
        })
        assets.append(asset)
    return assets

# Create production assets
prod_config = {
    "DatabaseConnection": "Server=prod-db;Database=mydb;",
    "ApiEndpoint": "https://api.prod.example.com",
    "CacheServer": "prod-cache:6379"
}
prod_assets = create_environment_assets("Production", prod_config)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create asset with duplicate name
    client.assets.create({
        "Name": "ExistingAsset",
        "ValueType": "Text",
        "Value": "test"
    })
except HTTPError as e:
    if e.response.status_code == 409:
        print("Asset with this name already exists")
    else:
        print(f"Error creating asset: {e}")
```

## Best Practices

1. Use meaningful asset names that reflect their purpose
2. Include clear descriptions for better maintainability
3. Use appropriate value types for different kinds of data
4. Consider using `PerRobot` scope for configuration that varies by robot
5. Protect sensitive information using Credential type assets
6. Group related assets using consistent naming conventions
7. Regularly review and update asset values
8. Use error handling when working with assets
9. Document asset dependencies in your processes

## Security Considerations

1. Use Credential/WindowsCredential types for sensitive data
2. Limit access to assets using folder permissions
3. Audit asset usage regularly
4. Update credentials stored in assets periodically
5. Be cautious with global-scope assets containing sensitive data

## See Also
- [UiPath Assets Documentation](https://docs.uipath.com/orchestrator/docs/about-assets)
- [Managing Robot Assets](https://docs.uipath.com/orchestrator/docs/managing-robot-assets)
- [Asset Security](https://docs.uipath.com/orchestrator/docs/asset-security) 
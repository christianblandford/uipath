# Licensing

The Licensing resource allows you to manage UiPath licenses, including viewing license information, managing license assignments, and monitoring license usage.

## Related Resources
- [Robots](robots.md) - Robots requiring licenses
- [Machines](machines.md) - Machines using licenses
- [Status](status.md) - System license status

## Methods

### get_license_info()
Get detailed information about the current license.

```python
info = client.licensing.get_license_info()
```

#### Returns
Dict: License information including:
- License type
- Expiration date
- Total available licenses
- Used licenses
- Features enabled

### get_license_status()
Get the current status of license usage.

```python
status = client.licensing.get_license_status()
```

#### Returns
Dict: License status including:
- Active licenses
- Available licenses
- Usage statistics
- Compliance status

### assign_license()
Assign a license to a robot or machine.

```python
client.licensing.assign_license(
    target_id=123,
    target_type="Robot",
    license_type="Unattended"
)
```

#### Parameters
- `target_id` (int): ID of robot or machine
- `target_type` (str): Type of target ("Robot" or "Machine")
- `license_type` (str): Type of license to assign

### revoke_license()
Revoke a license from a robot or machine.

```python
client.licensing.revoke_license(
    target_id=123,
    target_type="Robot"
)
```

#### Parameters
- `target_id` (int): ID of robot or machine
- `target_type` (str): Type of target ("Robot" or "Machine")

## Examples

### License Management

```python
def manage_licenses():
    """Manage and monitor license usage"""
    # Get current license status
    status = client.licensing.get_license_status()
    
    # Calculate usage percentage
    usage_percent = (
        status["UsedLicenses"] / status["TotalLicenses"] * 100
    )
    
    # Check if we need more licenses
    if usage_percent > 90:
        print(f"Warning: License usage at {usage_percent}%")
        
    # Get detailed info
    info = client.licensing.get_license_info()
    
    return {
        "usage_percent": usage_percent,
        "expires_on": info["ExpirationDate"],
        "features": info["Features"],
        "compliance": info["IsCompliant"]
    }

# Check license status
license_status = manage_licenses()
```

### License Assignment

```python
def assign_robot_licenses(robots: List[Dict]):
    """Assign licenses to robots"""
    results = []
    
    for robot in robots:
        try:
            # Assign appropriate license type
            client.licensing.assign_license(
                target_id=robot["Id"],
                target_type="Robot",
                license_type=robot["LicenseType"]
            )
            
            results.append({
                "robot_id": robot["Id"],
                "status": "assigned",
                "license_type": robot["LicenseType"]
            })
            
        except Exception as e:
            results.append({
                "robot_id": robot["Id"],
                "status": "error",
                "error": str(e)
            })
    
    return results

# Assign licenses
robots = [
    {"Id": 123, "LicenseType": "Attended"},
    {"Id": 456, "LicenseType": "Unattended"}
]
results = assign_robot_licenses(robots)
```

### License Optimization

```python
def optimize_license_usage():
    """Optimize license usage by reviewing assignments"""
    # Get all robots
    robots = client.robots.get()
    inactive_period = timedelta(days=30)
    
    optimizations = []
    for robot in robots:
        # Check last activity
        if robot.get("LicenseKey"):
            last_seen = datetime.fromisoformat(robot["LastSeen"])
            if datetime.now() - last_seen > inactive_period:
                try:
                    # Revoke license from inactive robot
                    client.licensing.revoke_license(
                        target_id=robot["Id"],
                        target_type="Robot"
                    )
                    
                    optimizations.append({
                        "robot_id": robot["Id"],
                        "action": "revoked",
                        "reason": "inactive",
                        "inactive_days": (datetime.now() - last_seen).days
                    })
                    
                except Exception as e:
                    print(f"Error optimizing robot {robot['Id']}: {e}")
    
    return optimizations

# Optimize licenses
optimizations = optimize_license_usage()
```

### License Monitoring

```python
def monitor_license_compliance():
    """Monitor license compliance and usage"""
    info = client.licensing.get_license_info()
    status = client.licensing.get_license_status()
    
    alerts = []
    
    # Check expiration
    if info["ExpirationDate"]:
        expiration = datetime.fromisoformat(info["ExpirationDate"])
        days_remaining = (expiration - datetime.now()).days
        
        if days_remaining < 30:
            alerts.append({
                "type": "expiration",
                "message": f"License expires in {days_remaining} days",
                "severity": "high"
            })
    
    # Check usage
    if status["UsedLicenses"] > status["TotalLicenses"]:
        alerts.append({
            "type": "overuse",
            "message": "More licenses used than available",
            "severity": "critical"
        })
    
    # Check compliance
    if not info["IsCompliant"]:
        alerts.append({
            "type": "compliance",
            "message": "License compliance issue detected",
            "severity": "critical"
        })
    
    return alerts

# Monitor compliance
alerts = monitor_license_compliance()
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to assign license
    client.licensing.assign_license(
        target_id=123,
        target_type="Robot",
        license_type="Unattended"
    )
except HTTPError as e:
    if e.response.status_code == 409:
        print("No licenses available")
    elif e.response.status_code == 400:
        print("Invalid license assignment")
    else:
        print(f"Error managing license: {e}")
```

## Best Practices

1. Regular license audits
2. Monitor usage trends
3. Plan for renewals
4. Document assignments
5. Regular optimization
6. Track compliance
7. Maintain buffer capacity
8. Monitor expiration dates
9. Review inactive licenses

## Security Considerations

1. Control license management access
2. Audit license changes
3. Secure license information
4. Monitor unusual activity
5. Regular compliance checks
6. Document license policies
7. Protect license keys

## See Also
- [UiPath Licensing Documentation](https://docs.uipath.com/orchestrator/docs/about-licensing)
- [License Management](https://docs.uipath.com/orchestrator/docs/managing-licenses)
- [License Types](https://docs.uipath.com/orchestrator/docs/license-types)
- [Robots](robots.md) for robot management
- [Status](status.md) for system status 
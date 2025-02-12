# Status

The Status resource allows you to monitor the health and operational status of UiPath Orchestrator components and services.

## Related Resources
- [Maintenance](settings/maintenance.md) - System maintenance operations
- [Stats](stats.md) - System statistics and metrics
- [Logs](logs.md) - System and process logs

## Methods

### get_status()
Get the overall system status.

```python
status = client.status.get_status()
```

#### Returns
Dict: System status information including:
- Service health
- Component status
- Version information
- License status

### get_license_status()
Get the status of system licensing.

```python
license_status = client.status.get_license_status()
```

#### Returns
Dict: License status information including:
- License validity
- Expiration details
- Usage metrics
- Compliance status

### get_component_status()
Get status of specific system components.

```python
components = client.status.get_component_status()
```

#### Returns
Dict: Status of various system components including:
- Web API
- Job Service
- Queues
- Storage
- Database

### get_version()
Get system version information.

```python
version = client.status.get_version()
```

#### Returns
Dict: Version information including:
- Orchestrator version
- API version
- Database version

## Examples

### System Health Check

```python
def check_system_health():
    """Comprehensive system health check"""
    results = {
        "status": client.status.get_status(),
        "license": client.status.get_license_status(),
        "components": client.status.get_component_status(),
        "version": client.status.get_version()
    }
    
    # Analyze health status
    health_summary = {
        "is_healthy": all(
            component["IsHealthy"]
            for component in results["components"]
        ),
        "license_valid": results["license"]["IsValid"],
        "version": results["version"]["Version"],
        "timestamp": datetime.now().isoformat()
    }
    
    return health_summary

# Run health check
health = check_system_health()
```

### Component Monitoring

```python
def monitor_components(threshold_minutes: int = 5):
    """Monitor component status with alerts"""
    components = client.status.get_component_status()
    alerts = []
    
    for component in components:
        # Check component health
        if not component["IsHealthy"]:
            alerts.append({
                "component": component["Name"],
                "status": "Unhealthy",
                "message": component.get("Message", "No details available")
            })
        
        # Check last heartbeat
        last_heartbeat = datetime.fromisoformat(component["LastHeartbeat"])
        if (datetime.now() - last_heartbeat).total_seconds() > threshold_minutes * 60:
            alerts.append({
                "component": component["Name"],
                "status": "Delayed Heartbeat",
                "last_seen": last_heartbeat.isoformat()
            })
    
    return alerts

# Monitor components
alerts = monitor_components(threshold_minutes=5)
```

### License Monitoring

```python
def monitor_license_status(warning_days: int = 30):
    """Monitor license status with warnings"""
    license_status = client.status.get_license_status()
    warnings = []
    
    # Check expiration
    if license_status["ExpirationDate"]:
        expiration = datetime.fromisoformat(license_status["ExpirationDate"])
        days_remaining = (expiration - datetime.now()).days
        
        if days_remaining <= warning_days:
            warnings.append({
                "type": "License Expiration",
                "message": f"License expires in {days_remaining} days",
                "expiration": expiration.isoformat()
            })
    
    # Check usage
    if license_status["UsedLicenses"] > license_status["AllowedLicenses"] * 0.9:
        warnings.append({
            "type": "License Usage",
            "message": "License usage above 90%",
            "used": license_status["UsedLicenses"],
            "total": license_status["AllowedLicenses"]
        })
    
    return warnings

# Monitor license status
license_warnings = monitor_license_status()
```

### Version Management

```python
def check_version_compatibility():
    """Check version compatibility across components"""
    version_info = client.status.get_version()
    
    compatibility = {
        "orchestrator": version_info["Version"],
        "api": version_info["ApiVersion"],
        "database": version_info["DatabaseVersion"],
        "is_compatible": all([
            version_info["IsApiVersionCompatible"],
            version_info["IsDatabaseVersionCompatible"]
        ]),
        "warnings": []
    }
    
    if not version_info["IsApiVersionCompatible"]:
        compatibility["warnings"].append("API version mismatch")
    if not version_info["IsDatabaseVersionCompatible"]:
        compatibility["warnings"].append("Database version mismatch")
    
    return compatibility

# Check version compatibility
version_status = check_version_compatibility()
```

## Error Handling

```python
from requests.exceptions import HTTPError, RequestException

def safe_status_check():
    try:
        status = client.status.get_status()
        return {
            "success": True,
            "status": status
        }
    except HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP Error: {e.response.status_code}",
            "message": str(e)
        }
    except RequestException as e:
        return {
            "success": False,
            "error": "Connection Error",
            "message": str(e)
        }

# Safe status check
result = safe_status_check()
```

## Best Practices

1. Regular health checks
2. Monitor component heartbeats
3. Track license usage trends
4. Set up alerts for issues
5. Document version requirements
6. Regular compatibility checks
7. Monitor system performance
8. Keep status logs
9. Plan for maintenance windows

## Security Considerations

1. Secure status endpoints
2. Monitor access attempts
3. Validate component authenticity
4. Protect status information
5. Audit system changes
6. Monitor security components
7. Track authorization status

## See Also
- [UiPath Status Documentation](https://docs.uipath.com/orchestrator/docs/monitoring-orchestrator)
- [System Monitoring](https://docs.uipath.com/orchestrator/docs/monitoring-and-alerting)
- [License Management](https://docs.uipath.com/orchestrator/docs/managing-licenses)
- [Maintenance](settings/maintenance.md) for system maintenance
- [Stats](stats.md) for detailed metrics 
# Alerts

The Alerts resource allows you to manage UiPath Orchestrator alerts and notifications for system events, job failures, and resource status changes.

## Related Resources
- [Jobs](jobs.md) - Jobs that generate alerts
- [Robots](robots.md) - Robot status alerts
- [Queues](queues.md) - Queue processing alerts
- [Status](status.md) - System status alerts

## Methods

### get()
Get a list of alerts with optional filters.

```python
alerts = client.alerts.get(
    severity="Critical",     # Filter by severity
    status="Active",        # Filter by status
    from_date="2023-01-01"  # Filter by date
)
```

#### Parameters
- `severity` (str, optional): Filter by severity (Critical, Warning, Info)
- `status` (str, optional): Filter by status (Active, Acknowledged, Resolved)
- `from_date` (str, optional): Filter by date (ISO format)

#### Returns
List[Dict]: List of alert objects matching the filters

### get_by_id()
Get a specific alert by ID.

```python
alert = client.alerts.get_by_id(123)
```

#### Parameters
- `alert_id` (int): ID of the alert to retrieve

#### Returns
Dict: Alert details

### acknowledge()
Acknowledge an alert.

```python
client.alerts.acknowledge(
    alert_id=123,
    notes="Investigating the issue"
)
```

#### Parameters
- `alert_id` (int): ID of the alert
- `notes` (str, optional): Acknowledgment notes

### resolve()
Resolve an alert.

```python
client.alerts.resolve(
    alert_id=123,
    resolution="Issue fixed by restarting service"
)
```

#### Parameters
- `alert_id` (int): ID of the alert
- `resolution` (str, optional): Resolution details

## Examples

### Alert Monitoring

```python
def monitor_critical_alerts():
    """Monitor and handle critical alerts"""
    alerts = client.alerts.get(
        severity="Critical",
        status="Active"
    )
    
    handled = []
    for alert in alerts:
        try:
            # Check alert type
            if alert["Type"] == "JobFaulted":
                # Handle job failure
                job_id = alert["EntityId"]
                job = client.jobs.get_by_id(job_id)
                
                if job["State"] == "Faulted":
                    # Attempt job retry
                    client.jobs.start_jobs(
                        release_key=job["ReleaseKey"],
                        robot_ids=[job["RobotId"]]
                    )
                    
            elif alert["Type"] == "RobotOffline":
                # Handle robot offline
                robot_id = alert["EntityId"]
                robot = client.robots.get_by_id(robot_id)
                
                if not robot["IsOnline"]:
                    # Notify admin
                    print(f"Robot {robot['Name']} is offline")
            
            # Acknowledge the alert
            client.alerts.acknowledge(
                alert["Id"],
                notes="Automated handling initiated"
            )
            
            handled.append({
                "alert_id": alert["Id"],
                "type": alert["Type"],
                "status": "handled"
            })
            
        except Exception as e:
            handled.append({
                "alert_id": alert["Id"],
                "type": alert["Type"],
                "status": "error",
                "error": str(e)
            })
    
    return handled

# Monitor alerts
handled_alerts = monitor_critical_alerts()
```

### Alert Aggregation

```python
def aggregate_alerts(time_window: int = 24):
    """Aggregate alerts for reporting"""
    from datetime import datetime, timedelta
    
    start_date = (datetime.now() - timedelta(hours=time_window)).isoformat()
    alerts = client.alerts.get(from_date=start_date)
    
    # Aggregate by type and severity
    aggregation = {
        "by_type": {},
        "by_severity": {},
        "total_count": len(alerts),
        "active_count": 0,
        "window_hours": time_window
    }
    
    for alert in alerts:
        # Aggregate by type
        alert_type = alert["Type"]
        if alert_type not in aggregation["by_type"]:
            aggregation["by_type"][alert_type] = 0
        aggregation["by_type"][alert_type] += 1
        
        # Aggregate by severity
        severity = alert["Severity"]
        if severity not in aggregation["by_severity"]:
            aggregation["by_severity"][severity] = 0
        aggregation["by_severity"][severity] += 1
        
        # Count active alerts
        if alert["Status"] == "Active":
            aggregation["active_count"] += 1
    
    return aggregation

# Aggregate alerts
alert_stats = aggregate_alerts(time_window=24)
```

### Alert Auto-Resolution

```python
def auto_resolve_alerts(max_age_hours: int = 48):
    """Auto-resolve old alerts based on conditions"""
    from datetime import datetime, timedelta
    
    cutoff_date = (datetime.now() - timedelta(hours=max_age_hours)).isoformat()
    old_alerts = client.alerts.get(
        status="Active",
        from_date=cutoff_date
    )
    
    resolutions = []
    for alert in old_alerts:
        try:
            # Check if alert can be auto-resolved
            if alert["Severity"] != "Critical":
                # Resolve non-critical old alerts
                client.alerts.resolve(
                    alert["Id"],
                    resolution=f"Auto-resolved after {max_age_hours} hours"
                )
                
                resolutions.append({
                    "alert_id": alert["Id"],
                    "status": "resolved",
                    "age_hours": max_age_hours
                })
                
        except Exception as e:
            resolutions.append({
                "alert_id": alert["Id"],
                "status": "error",
                "error": str(e)
            })
    
    return resolutions

# Auto-resolve old alerts
resolutions = auto_resolve_alerts(max_age_hours=48)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to resolve already resolved alert
    client.alerts.resolve(123, "Issue fixed")
except HTTPError as e:
    if e.response.status_code == 400:
        print("Alert already resolved")
    elif e.response.status_code == 404:
        print("Alert not found")
    else:
        print(f"Error handling alert: {e}")
```

## Best Practices

1. Monitor critical alerts promptly
2. Set up alert notifications
3. Document alert handling procedures
4. Regular alert cleanup
5. Track alert patterns
6. Automate common resolutions
7. Maintain alert history
8. Set appropriate severity levels
9. Configure alert thresholds

## Security Considerations

1. Control alert access
2. Audit alert handling
3. Secure alert data
4. Monitor alert patterns
5. Validate alert sources
6. Protect sensitive information
7. Regular security reviews

## See Also
- [UiPath Alerts Documentation](https://docs.uipath.com/orchestrator/docs/about-alerts)
- [Alert Management](https://docs.uipath.com/orchestrator/docs/managing-alerts)
- [Notification Settings](https://docs.uipath.com/orchestrator/docs/notification-settings)
- [Jobs](jobs.md) for job monitoring
- [Status](status.md) for system monitoring 
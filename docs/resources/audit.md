# Audit

The Audit resource allows you to access and manage UiPath Orchestrator audit logs, tracking system changes, user actions, and security events.

## Related Resources
- [Directory](directory.md) - User actions being audited
- [Settings](settings.md) - System configuration changes
- [Logs](logs.md) - Process execution logs

## Methods

### get_audit_logs()
Get audit logs with optional filters.

```python
logs = client.audit.get_audit_logs(
    from_date="2023-01-01",
    to_date="2023-12-31",
    component="Settings",
    action="Update"
)
```

#### Parameters
- `from_date` (str, optional): Start date for logs (ISO format)
- `to_date` (str, optional): End date for logs (ISO format)
- `component` (str, optional): Filter by component
- `action` (str, optional): Filter by action type

#### Returns
List[Dict]: List of audit log entries

### get_audit_trail()
Get detailed audit trail for a specific entity.

```python
trail = client.audit.get_audit_trail(
    entity_type="Robot",
    entity_id=123
)
```

#### Parameters
- `entity_type` (str): Type of entity
- `entity_id` (int): ID of the entity

#### Returns
List[Dict]: Audit trail entries

### export_audit_logs()
Export audit logs to a file.

```python
client.audit.export_audit_logs(
    from_date="2023-01-01",
    to_date="2023-12-31",
    format="CSV"
)
```

#### Parameters
- `from_date` (str): Start date for export
- `to_date` (str): End date for export
- `format` (str): Export format ("CSV" or "JSON")

## Examples

### Security Audit

```python
def audit_security_changes(days: int = 30):
    """Audit security-related changes"""
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get security-related logs
    logs = client.audit.get_audit_logs(
        from_date=start_date.isoformat(),
        to_date=end_date.isoformat(),
        component="Security"
    )
    
    # Analyze changes
    findings = []
    for log in logs:
        if log["Action"] in ["PermissionChange", "RoleModification", "UserAccess"]:
            findings.append({
                "timestamp": log["Timestamp"],
                "user": log["InitiatedBy"],
                "action": log["Action"],
                "details": log["Details"],
                "severity": "high"
            })
    
    return findings

# Audit security changes
security_findings = audit_security_changes()
```

### Configuration Change Tracking

```python
def track_config_changes():
    """Track configuration changes"""
    # Get configuration change logs
    logs = client.audit.get_audit_logs(
        component="Settings",
        action="Update"
    )
    
    # Group changes by user
    changes_by_user = {}
    for log in logs:
        user = log["InitiatedBy"]
        if user not in changes_by_user:
            changes_by_user[user] = []
            
        changes_by_user[user].append({
            "timestamp": log["Timestamp"],
            "setting": log["EntityType"],
            "old_value": log.get("OldValue"),
            "new_value": log.get("NewValue")
        })
    
    return changes_by_user

# Track configuration changes
changes = track_config_changes()
```

### User Activity Monitoring

```python
def monitor_user_activity(user_id: int, days: int = 7):
    """Monitor specific user activity"""
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get user's audit trail
    trail = client.audit.get_audit_trail(
        entity_type="User",
        entity_id=user_id
    )
    
    # Analyze activity
    activity = {
        "login_attempts": 0,
        "configuration_changes": 0,
        "resource_access": 0,
        "suspicious_actions": []
    }
    
    for entry in trail:
        if entry["Action"] == "Login":
            activity["login_attempts"] += 1
        elif entry["Action"].endswith("Update"):
            activity["configuration_changes"] += 1
        elif entry["Action"].startswith("Access"):
            activity["resource_access"] += 1
            
        # Check for suspicious activity
        if entry.get("Status") == "Failed" or entry.get("Severity") == "High":
            activity["suspicious_actions"].append({
                "timestamp": entry["Timestamp"],
                "action": entry["Action"],
                "details": entry["Details"]
            })
    
    return activity

# Monitor user activity
activity_report = monitor_user_activity(user_id=123)
```

### Compliance Reporting

```python
def generate_compliance_report(report_period: str):
    """Generate compliance audit report"""
    # Get all relevant audit logs
    logs = client.audit.get_audit_logs()
    
    report = {
        "period": report_period,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_events": len(logs),
            "security_events": 0,
            "compliance_violations": 0,
            "user_access_events": 0
        },
        "violations": [],
        "access_patterns": {}
    }
    
    # Analyze logs
    for log in logs:
        # Track security events
        if log["Component"] == "Security":
            report["summary"]["security_events"] += 1
            
        # Track access events
        if log["Action"].startswith("Access"):
            report["summary"]["user_access_events"] += 1
            user = log["InitiatedBy"]
            if user not in report["access_patterns"]:
                report["access_patterns"][user] = 0
            report["access_patterns"][user] += 1
            
        # Track compliance violations
        if log.get("ComplianceStatus") == "Violation":
            report["summary"]["compliance_violations"] += 1
            report["violations"].append({
                "timestamp": log["Timestamp"],
                "user": log["InitiatedBy"],
                "action": log["Action"],
                "details": log["Details"]
            })
    
    return report

# Generate compliance report
report = generate_compliance_report("Q4 2023")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to access audit logs
    logs = client.audit.get_audit_logs(
        from_date="2023-01-01",
        to_date="2023-12-31"
    )
except HTTPError as e:
    if e.response.status_code == 403:
        print("Insufficient permissions to access audit logs")
    elif e.response.status_code == 400:
        print("Invalid date range")
    else:
        print(f"Error accessing audit logs: {e}")
```

## Best Practices

1. Regular audit log review
2. Set appropriate retention periods
3. Monitor security events
4. Document audit findings
5. Maintain audit trails
6. Export logs regularly
7. Track configuration changes
8. Monitor user activity
9. Generate compliance reports

## Security Considerations

1. Protect audit logs
2. Control audit access
3. Monitor unauthorized access
4. Secure log exports
5. Maintain log integrity
6. Track sensitive operations
7. Regular security audits

## See Also
- [UiPath Audit Documentation](https://docs.uipath.com/orchestrator/docs/about-audit)
- [Security Auditing](https://docs.uipath.com/orchestrator/docs/security-audit)
- [Compliance](https://docs.uipath.com/orchestrator/docs/compliance)
- [Directory](directory.md) for user management
- [Settings](settings.md) for configuration 
# Schedules

The Schedules resource allows you to manage automated job scheduling in UiPath Orchestrator. Schedules enable you to run processes automatically based on time-based triggers.

## Related Resources
- [Jobs](jobs.md) - Jobs created by schedules
- [Processes](processes.md) - Processes run by schedules
- [Robots](robots.md) - Robots executing scheduled jobs

## Methods

### get()
Get a list of schedules with optional filters.

```python
schedules = client.schedules.get(
    enabled=True,           # Filter by enabled status
    process_key="MyProcess" # Filter by process
)
```

#### Parameters
- `enabled` (bool, optional): Filter by enabled status
- `process_key` (str, optional): Filter by process key

#### Returns
List[Dict]: List of schedule objects matching the filters

### get_by_id()
Get a specific schedule by ID.

```python
schedule = client.schedules.get_by_id(123)
```

#### Parameters
- `schedule_id` (int): ID of the schedule to retrieve

#### Returns
Dict: Schedule details

### create()
Create a new schedule.

```python
schedule = client.schedules.create({
    "Name": "DailyReport",
    "ReleaseKey": "release-key-123",
    "Enabled": True,
    "TimeZoneId": "UTC",
    "CronExpression": "0 0 8 * * ?",  # 8 AM daily
    "StartProcessCron": {
        "RobotIds": [123, 456],
        "JobPriority": "Normal",
        "Strategy": "Specific"
    }
})
```

#### Parameters
- `schedule_data` (Dict): Schedule configuration including:
  - `Name` (str, required): Schedule name
  - `ReleaseKey` (str, required): Process release key
  - `Enabled` (bool, required): Whether schedule is enabled
  - `TimeZoneId` (str, required): Timezone for schedule
  - `CronExpression` (str, required): Cron expression for timing
  - `StartProcessCron` (Dict, required): Process execution settings

#### Returns
Dict: Created schedule details

### update()
Update an existing schedule.

```python
client.schedules.update(123, {
    "Enabled": False,
    "CronExpression": "0 0 9 * * ?"  # Change to 9 AM
})
```

#### Parameters
- `schedule_id` (int): ID of schedule to update
- `schedule_data` (Dict): Updated schedule data

### delete()
Delete a schedule.

```python
client.schedules.delete(123)
```

#### Parameters
- `schedule_id` (int): ID of schedule to delete

## Examples

### Schedule Creation

```python
def create_business_hours_schedule(process_key: str, robot_ids: List[int]):
    """Create schedule for business hours execution"""
    schedule = client.schedules.create({
        "Name": f"{process_key}_BusinessHours",
        "ReleaseKey": process_key,
        "Enabled": True,
        "TimeZoneId": "America/New_York",
        "CronExpression": "0 0 9-17 ? * MON-FRI",  # 9 AM to 5 PM weekdays
        "StartProcessCron": {
            "RobotIds": robot_ids,
            "JobPriority": "Normal",
            "Strategy": "Specific",
            "InputArguments": {
                "BusinessHours": True
            }
        }
    })
    
    return schedule

# Create business hours schedule
schedule = create_business_hours_schedule(
    process_key="process-key-123",
    robot_ids=[123, 456]
)
```

### Schedule Management

```python
def manage_schedule_status(schedule_id: int, active_hours: tuple):
    """Enable/disable schedule based on hours"""
    from datetime import datetime
    
    current_hour = datetime.now().hour
    start_hour, end_hour = active_hours
    
    # Get current schedule
    schedule = client.schedules.get_by_id(schedule_id)
    
    # Check if schedule should be enabled
    should_be_enabled = start_hour <= current_hour < end_hour
    
    if schedule["Enabled"] != should_be_enabled:
        client.schedules.update(schedule_id, {
            "Enabled": should_be_enabled
        })
        
        return {
            "schedule_id": schedule_id,
            "status_changed": True,
            "now_enabled": should_be_enabled
        }
    
    return {
        "schedule_id": schedule_id,
        "status_changed": False,
        "now_enabled": schedule["Enabled"]
    }

# Manage schedule for business hours
result = manage_schedule_status(123, (9, 17))
```

### Cron Expression Management

```python
def update_schedule_timing(schedule_id: int, timing_config: Dict):
    """Update schedule timing configuration"""
    def build_cron_expression(config):
        # Convert timing config to cron expression
        minute = config.get("minute", "0")
        hour = config.get("hour", "*")
        day = config.get("day", "*")
        month = config.get("month", "*")
        weekday = config.get("weekday", "?")
        
        return f"{minute} {hour} {day} {month} {weekday}"
    
    cron_expression = build_cron_expression(timing_config)
    
    updated = client.schedules.update(schedule_id, {
        "CronExpression": cron_expression,
        "TimeZoneId": timing_config.get("timezone", "UTC")
    })
    
    return {
        "schedule_id": schedule_id,
        "new_expression": cron_expression,
        "timezone": updated["TimeZoneId"]
    }

# Update schedule timing
timing = {
    "minute": "0",
    "hour": "*/2",  # Every 2 hours
    "weekday": "MON-FRI",
    "timezone": "Europe/London"
}
result = update_schedule_timing(123, timing)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create schedule with invalid cron expression
    client.schedules.create({
        "Name": "InvalidSchedule",
        "ReleaseKey": "release-key-123",
        "CronExpression": "invalid",
        "TimeZoneId": "UTC",
        "Enabled": True
    })
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid schedule configuration")
    elif e.response.status_code == 404:
        print("Process release not found")
    else:
        print(f"Error creating schedule: {e}")
```

## Best Practices

1. Use descriptive schedule names
2. Consider timezone differences
3. Validate cron expressions
4. Monitor schedule execution
5. Document schedule purposes
6. Regular schedule review
7. Test schedule changes
8. Maintain execution logs
9. Consider resource availability

## Security Considerations

1. Control schedule access
2. Audit schedule changes
3. Monitor execution patterns
4. Validate process inputs
5. Review robot assignments
6. Regular security checks
7. Document access controls

## See Also
- [UiPath Schedules Documentation](https://docs.uipath.com/orchestrator/docs/about-schedules)
- [Cron Expression Guide](https://docs.uipath.com/orchestrator/docs/cron-expressions)
- [Schedule Management](https://docs.uipath.com/orchestrator/docs/managing-schedules)
- [Jobs](jobs.md) for job execution
- [Robots](robots.md) for robot management 
# Metrics

The Metrics resource allows you to access performance metrics and operational statistics from UiPath Orchestrator. These metrics help monitor system health, performance, and resource utilization.

## Related Resources
- [Stats](stats.md) - Detailed statistical data
- [Status](status.md) - System status information
- [Jobs](jobs.md) - Job performance metrics
- [Robots](robots.md) - Robot performance metrics

## Methods

### get_metrics()
Get system metrics with optional filters.

```python
metrics = client.metrics.get_metrics(
    category="Performance",    # Filter by category
    from_date="2023-01-01",   # Start date
    to_date="2023-12-31"      # End date
)
```

#### Parameters
- `category` (str, optional): Filter by metric category
- `from_date` (str, optional): Start date for metrics (ISO format)
- `to_date` (str, optional): End date for metrics (ISO format)

#### Returns
Dict: System metrics data

### get_performance_metrics()
Get performance-specific metrics.

```python
performance = client.metrics.get_performance_metrics()
```

#### Returns
Dict: Performance metrics including:
- Response times
- Resource utilization
- Throughput statistics
- Error rates

### get_resource_metrics()
Get resource utilization metrics.

```python
resources = client.metrics.get_resource_metrics()
```

#### Returns
Dict: Resource metrics including:
- CPU usage
- Memory utilization
- Storage usage
- Network statistics

## Examples

### Performance Monitoring

```python
def monitor_system_performance(threshold_minutes: int = 5):
    """Monitor system performance metrics"""
    metrics = client.metrics.get_performance_metrics()
    
    alerts = []
    
    # Check response times
    if metrics["AverageResponseTime"] > threshold_minutes * 60:
        alerts.append({
            "metric": "response_time",
            "value": metrics["AverageResponseTime"],
            "threshold": threshold_minutes * 60,
            "severity": "high"
        })
    
    # Check error rates
    if metrics["ErrorRate"] > 0.05:  # 5% threshold
        alerts.append({
            "metric": "error_rate",
            "value": metrics["ErrorRate"],
            "threshold": 0.05,
            "severity": "high"
        })
    
    # Check throughput
    if metrics["RequestsPerMinute"] < 10:
        alerts.append({
            "metric": "throughput",
            "value": metrics["RequestsPerMinute"],
            "threshold": 10,
            "severity": "medium"
        })
    
    return {
        "metrics": metrics,
        "alerts": alerts,
        "timestamp": datetime.now().isoformat()
    }

# Monitor performance
performance_status = monitor_system_performance()
```

### Resource Utilization

```python
def analyze_resource_usage():
    """Analyze resource utilization patterns"""
    metrics = client.metrics.get_resource_metrics()
    
    analysis = {
        "cpu": {
            "current": metrics["CpuUsage"],
            "peak": metrics["PeakCpuUsage"],
            "average": metrics["AverageCpuUsage"]
        },
        "memory": {
            "current": metrics["MemoryUsage"],
            "available": metrics["AvailableMemory"],
            "total": metrics["TotalMemory"]
        },
        "storage": {
            "used": metrics["StorageUsed"],
            "available": metrics["StorageAvailable"],
            "critical_paths": []
        }
    }
    
    # Check for storage hotspots
    for path, usage in metrics["StorageByPath"].items():
        if usage["UsedPercentage"] > 85:
            analysis["storage"]["critical_paths"].append({
                "path": path,
                "usage_percent": usage["UsedPercentage"]
            })
    
    return analysis

# Analyze resources
resource_analysis = analyze_resource_usage()
```

### Metric Trending

```python
def analyze_metric_trends(days: int = 30):
    """Analyze metric trends over time"""
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    metrics = client.metrics.get_metrics(
        from_date=start_date.isoformat(),
        to_date=end_date.isoformat()
    )
    
    trends = {
        "performance": {
            "response_time": [],
            "error_rate": [],
            "throughput": []
        },
        "resources": {
            "cpu_usage": [],
            "memory_usage": [],
            "storage_usage": []
        }
    }
    
    # Analyze daily patterns
    for day_metrics in metrics["DailyMetrics"]:
        date = day_metrics["Date"]
        
        # Performance trends
        trends["performance"]["response_time"].append({
            "date": date,
            "value": day_metrics["AverageResponseTime"]
        })
        
        trends["performance"]["error_rate"].append({
            "date": date,
            "value": day_metrics["ErrorRate"]
        })
        
        # Resource trends
        trends["resources"]["cpu_usage"].append({
            "date": date,
            "value": day_metrics["AverageCpuUsage"]
        })
    
    return trends

# Analyze trends
metric_trends = analyze_metric_trends()
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to get metrics with invalid date range
    metrics = client.metrics.get_metrics(
        from_date="invalid-date"
    )
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid date format")
    elif e.response.status_code == 403:
        print("Insufficient permissions to access metrics")
    else:
        print(f"Error retrieving metrics: {e}")
```

## Best Practices

1. Regular metric collection
2. Set appropriate thresholds
3. Monitor trends over time
4. Document baseline metrics
5. Alert on anomalies
6. Retain historical data
7. Regular metric review
8. Correlate with events
9. Validate metric accuracy

## Security Considerations

1. Control metric access
2. Secure metric data
3. Audit metric access
4. Validate data sources
5. Monitor suspicious patterns
6. Protect sensitive metrics
7. Regular security review

## See Also
- [UiPath Monitoring Documentation](https://docs.uipath.com/orchestrator/docs/monitoring-and-metrics)
- [Performance Monitoring](https://docs.uipath.com/orchestrator/docs/performance-monitoring)
- [Resource Management](https://docs.uipath.com/orchestrator/docs/resource-management)
- [Stats](stats.md) for detailed statistics
- [Status](status.md) for system status 
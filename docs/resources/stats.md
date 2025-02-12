# Stats

The Stats resource provides detailed statistics and metrics about UiPath Orchestrator operations, including job execution, license usage, and system performance.

## Related Resources
- [Status](status.md) - Overall system status
- [Jobs](jobs.md) - Job execution details
- [Robots](robots.md) - Robot performance metrics
- [Queues](queues.md) - Queue processing metrics

## Methods

### get_jobs_stats()
Get statistics about job execution.

```python
stats = client.stats.get_jobs_stats(
    from_date="2023-01-01",
    to_date="2023-12-31"
)
```

#### Parameters
- `from_date` (str, optional): Start date for stats (ISO format)
- `to_date` (str, optional): End date for stats (ISO format)

#### Returns
Dict: Job statistics including:
- Total jobs executed
- Success/failure rates
- Average execution time
- Peak execution times

### get_license_stats()
Get detailed license usage statistics.

```python
stats = client.stats.get_license_stats(days=30)
```

#### Parameters
- `days` (int, optional): Number of days to analyze (default: 30)

#### Returns
Dict: License statistics including:
- Daily usage patterns
- Peak usage periods
- Usage by license type
- Compliance metrics

### get_queue_stats()
Get statistics about queue processing.

```python
stats = client.stats.get_queue_stats(
    queue_name="InvoiceQueue"
)
```

#### Parameters
- `queue_name` (str, optional): Filter by specific queue

#### Returns
Dict: Queue statistics including:
- Items processed
- Processing times
- Success/failure rates
- Queue throughput

## Examples

### Job Performance Analysis

```python
def analyze_job_performance(days: int = 30):
    """Analyze job execution performance"""
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    stats = client.stats.get_jobs_stats(
        from_date=start_date.isoformat(),
        to_date=end_date.isoformat()
    )
    
    analysis = {
        "total_jobs": stats["TotalJobs"],
        "success_rate": stats["SuccessfulJobs"] / stats["TotalJobs"] * 100,
        "avg_duration": stats["AverageExecutionTime"],
        "peak_time": stats["PeakExecutionTime"],
        "period": f"{days} days",
        "timestamp": datetime.now().isoformat()
    }
    
    return analysis

# Analyze job performance
performance = analyze_job_performance(days=30)
```

### License Usage Trends

```python
def analyze_license_trends(days: int = 90):
    """Analyze license usage patterns"""
    stats = client.stats.get_license_stats(days=days)
    
    # Analyze daily patterns
    daily_usage = {}
    peak_usage = 0
    peak_date = None
    
    for day in stats["DailyUsage"]:
        usage = day["UsedLicenses"]
        date = datetime.fromisoformat(day["Date"])
        daily_usage[date.date().isoformat()] = usage
        
        if usage > peak_usage:
            peak_usage = usage
            peak_date = date
    
    return {
        "average_usage": sum(daily_usage.values()) / len(daily_usage),
        "peak_usage": peak_usage,
        "peak_date": peak_date.isoformat(),
        "usage_trend": daily_usage
    }

# Analyze license trends
trends = analyze_license_trends()
```

### Queue Performance Monitoring

```python
def monitor_queue_performance(queue_names: List[str]):
    """Monitor performance of multiple queues"""
    performance = {}
    
    for queue in queue_names:
        stats = client.stats.get_queue_stats(queue_name=queue)
        
        performance[queue] = {
            "processed_items": stats["ProcessedItems"],
            "success_rate": stats["SuccessRate"],
            "avg_processing_time": stats["AverageProcessingTime"],
            "throughput": stats["ItemsPerHour"]
        }
    
    return performance

# Monitor queues
queues = ["InvoiceQueue", "OrderQueue", "SupportQueue"]
queue_performance = monitor_queue_performance(queues)
```

### Performance Dashboard

```python
def generate_performance_dashboard():
    """Generate comprehensive performance dashboard"""
    dashboard = {
        "jobs": client.stats.get_jobs_stats(
            from_date=(datetime.now() - timedelta(days=7)).isoformat()
        ),
        "licenses": client.stats.get_license_stats(days=7),
        "queues": client.stats.get_queue_stats(),
        "generated_at": datetime.now().isoformat()
    }
    
    # Calculate key metrics
    dashboard["metrics"] = {
        "job_success_rate": (
            dashboard["jobs"]["SuccessfulJobs"] /
            dashboard["jobs"]["TotalJobs"] * 100
        ),
        "license_utilization": (
            dashboard["licenses"]["CurrentUsage"] /
            dashboard["licenses"]["TotalLicenses"] * 100
        ),
        "queue_efficiency": (
            dashboard["queues"]["SuccessfulItems"] /
            dashboard["queues"]["TotalItems"] * 100
        )
    }
    
    return dashboard

# Generate dashboard
dashboard = generate_performance_dashboard()
```

## Error Handling

```python
from requests.exceptions import HTTPError
from datetime import datetime, timedelta

def safe_stats_collection():
    try:
        # Collect all stats
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        return {
            "success": True,
            "data": {
                "jobs": client.stats.get_jobs_stats(
                    from_date=start_date.isoformat(),
                    to_date=end_date.isoformat()
                ),
                "licenses": client.stats.get_license_stats(),
                "queues": client.stats.get_queue_stats()
            }
        }
    except HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP Error: {e.response.status_code}",
            "message": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "General Error",
            "message": str(e)
        }
```

## Best Practices

1. Regular metrics collection
2. Trend analysis over time
3. Set performance baselines
4. Monitor peak usage periods
5. Track performance degradation
6. Document performance patterns
7. Set up alerting thresholds
8. Regular reporting
9. Historical data retention

## Security Considerations

1. Protect metrics data
2. Control access to statistics
3. Audit metric access
4. Secure reporting channels
5. Data retention policies
6. Metrics data privacy
7. Access logging

## See Also
- [UiPath Monitoring Documentation](https://docs.uipath.com/orchestrator/docs/monitoring-and-statistics)
- [Performance Optimization](https://docs.uipath.com/orchestrator/docs/performance-optimization)
- [Reporting](https://docs.uipath.com/orchestrator/docs/about-reporting)
- [Status](status.md) for system health
- [Jobs](jobs.md) for job management 
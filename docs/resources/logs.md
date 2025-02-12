# Logs

The Logs resource allows you to submit log entries to UiPath Orchestrator. This is useful for tracking process execution, debugging, and audit purposes.

## Related Resources
- [Jobs](jobs.md) - Jobs generate logs during execution
- [Robots](robots.md) - Robots generate logs during operation
- [Processes](processes.md) - Processes generate logs during execution

## Methods

### submit_logs()
Submit multiple log entries to Orchestrator.

```python
client.logs.submit_logs([
    {
        "message": "Process started",
        "level": "Information",
        "timeStamp": "2023-01-18T14:46:07.4152893+02:00",
        "windowsIdentity": "DESKTOP-1L50L0P\\WindowsUser",
        "processName": "InvoiceProcessing",
        "fileName": "Main.xaml",
        "jobId": "8066c309-cef8-4b47-9163-b273fc14cc43"
    },
    {
        "message": "Invoice processed successfully",
        "level": "Information",
        "timeStamp": "2023-01-18T14:47:07.4152893+02:00",
        "processName": "InvoiceProcessing"
    }
])
```

#### Parameters
- `logs` (List[str]): Collection of log entries. Each entry should include:
  - `message` (str, required): Log message
  - `level` (str, optional): Log level (Information, Warning, Error)
  - `timeStamp` (str, optional): ISO format timestamp
  - `windowsIdentity` (str, optional): Windows identity of the process
  - `agentSessionId` (str, optional): Session ID of the robot
  - `processName` (str, optional): Name of the process
  - `fileName` (str, optional): Name of the file generating the log
  - `jobId` (str, optional): Associated job ID

### post_log()
Submit a single log entry (Deprecated).

```python
client.logs.post_log({
    "message": "Process completed",
    "level": "Information",
    "timeStamp": "2023-01-18T14:46:07.4152893+02:00",
    "processName": "InvoiceProcessing"
})
```

#### Parameters
- `log_data` (Dict): Log entry data (same structure as individual entries in submit_logs)

!!! warning "Deprecation Notice"
    This method is deprecated. Use `submit_logs()` instead for better performance and reliability.

## Examples

### Basic Logging

```python
# Log process execution steps
client.logs.submit_logs([
    {
        "message": "Starting invoice processing",
        "level": "Information",
        "processName": "InvoiceProcessing",
        "timeStamp": "2023-01-18T14:46:07.4152893+02:00"
    },
    {
        "message": "Invoice validated",
        "level": "Information",
        "processName": "InvoiceProcessing",
        "timeStamp": "2023-01-18T14:46:08.4152893+02:00"
    }
])
```

### Error Logging

```python
import datetime
import traceback

def log_error(error: Exception, process_name: str):
    client.logs.submit_logs([{
        "message": str(error),
        "level": "Error",
        "timeStamp": datetime.datetime.now().isoformat(),
        "processName": process_name,
        "details": traceback.format_exc()
    }])

try:
    # Process logic here
    raise ValueError("Invalid invoice format")
except Exception as e:
    log_error(e, "InvoiceProcessing")
```

### Structured Logging

```python
def create_log_entry(
    message: str,
    level: str = "Information",
    process_name: str = None,
    **kwargs
) -> dict:
    entry = {
        "message": message,
        "level": level,
        "timeStamp": datetime.datetime.now().isoformat()
    }
    if process_name:
        entry["processName"] = process_name
    entry.update(kwargs)
    return entry

# Using the helper function
logs = [
    create_log_entry(
        "Process started",
        process_name="InvoiceProcessing",
        jobId="123"
    ),
    create_log_entry(
        "Processing invoice: INV-001",
        process_name="InvoiceProcessing",
        jobId="123"
    ),
    create_log_entry(
        "Process completed",
        process_name="InvoiceProcessing",
        jobId="123"
    )
]

client.logs.submit_logs(logs)
```

### Batch Logging

```python
def batch_submit_logs(logs, batch_size=100):
    """Submit logs in batches to avoid large requests"""
    for i in range(0, len(logs), batch_size):
        batch = logs[i:i + batch_size]
        client.logs.submit_logs(batch)

# Generate some logs
logs = [
    {
        "message": f"Processing item {i}",
        "level": "Information",
        "timeStamp": datetime.datetime.now().isoformat(),
        "processName": "BatchProcess"
    }
    for i in range(1000)
]

# Submit in batches
batch_submit_logs(logs)
```

## Error Handling

```python
from requests.exceptions import HTTPError, RequestException

def safe_submit_logs(logs):
    try:
        client.logs.submit_logs(logs)
    except HTTPError as e:
        if e.response.status_code == 408:
            print("Timeout - too many pending logging requests")
        else:
            print(f"HTTP error submitting logs: {e}")
    except RequestException as e:
        print(f"Error submitting logs: {e}")
```

## Best Practices

1. Use `submit_logs()` instead of `post_log()` for better performance
2. Include relevant context in logs (process name, job ID, etc.)
3. Use appropriate log levels:
   - Information: Normal operation
   - Warning: Potential issues
   - Error: Failures and exceptions
4. Include timestamps for accurate timing information
5. Batch log submissions for better performance
6. Handle log submission failures gracefully
7. Don't include sensitive information in logs

## See Also
- [UiPath Logging Documentation](https://docs.uipath.com/orchestrator/docs/about-logging)
- [Logging Best Practices](https://docs.uipath.com/orchestrator/docs/logging-best-practices)
- [Jobs](jobs.md) for job-specific logging 
# Jobs

The Jobs resource allows you to manage and monitor process executions in UiPath Orchestrator.

## Related Resources
- [Robots](robots.md) - Robots that execute jobs
- [Processes](processes.md) - Processes that can be executed as jobs
- [Releases](releases.md) - Process releases that jobs run
- [Queues](queues.md) - Queue items that can trigger jobs

## Methods

### get()
Get a list of jobs with optional filters.

```python
jobs = client.jobs.get(
    state="Successful",          # Filter by job state
    robot_name="MyRobot",        # Filter by robot name
    start_time="2023-01-01",     # Filter by start time
    end_time="2023-12-31"        # Filter by end time
)
```

#### Parameters
- `state` (str, optional): Filter by job state. Valid values:
  - `Pending`
  - `Running`
  - `Successful`
  - `Faulted`
  - `Stopped`
  - `Suspended`
  - `Resuming`
- `robot_name` (str, optional): Filter by robot name
- `start_time` (str, optional): Filter by start time (ISO format)
- `end_time` (str, optional): Filter by end time (ISO format)
- `process_name` (str, optional): Filter by process name
- `source` (str, optional): Filter by job source

#### Returns
List[Dict]: List of job objects matching the filters

### get_by_id()
Get a specific job by ID.

```python
job = client.jobs.get_by_id(123)
```

#### Parameters
- `job_id` (int): ID of the job to retrieve

#### Returns
Dict: Job details

### start_jobs()
Start one or more jobs.

```python
jobs = client.jobs.start_jobs({
    "startInfo": {
        "ReleaseKey": "release_key",
        "Strategy": "Specific",
        "RobotIds": [123, 456],
        "InputArguments": {
            "param1": "value1"
        }
    }
})
```

#### Parameters
- `start_info` (Dict): Job start configuration including:
  - `ReleaseKey` (str, required): Release key to execute
  - `Strategy` (str, required): Robot selection strategy
  - `RobotIds` (List[int], optional): Specific robots to use
  - `InputArguments` (Dict, optional): Process input parameters

#### Returns
Dict: Started job details

[... continue with other methods and examples ...] 
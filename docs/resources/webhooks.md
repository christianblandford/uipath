# Webhooks

The Webhooks resource allows you to configure and manage webhook integrations in UiPath Orchestrator. Webhooks enable real-time notifications about events to external systems.

## Related Resources
- [Jobs](jobs.md) - Job events that trigger webhooks
- [Robots](robots.md) - Robot events that trigger webhooks
- [Queues](queues.md) - Queue events that trigger webhooks

## Methods

### get()
Get a list of webhook subscriptions.

```python
webhooks = client.webhooks.get(
    enabled=True,           # Filter by enabled status
    event_type="Job.Completed"  # Filter by event type
)
```

#### Parameters
- `enabled` (bool, optional): Filter by enabled status
- `event_type` (str, optional): Filter by event type

#### Returns
List[Dict]: List of webhook subscriptions

### get_by_id()
Get a specific webhook subscription by ID.

```python
webhook = client.webhooks.get_by_id(123)
```

#### Parameters
- `webhook_id` (int): ID of the webhook to retrieve

#### Returns
Dict: Webhook subscription details

### create()
Create a new webhook subscription.

```python
webhook = client.webhooks.create({
    "Name": "JobNotifier",
    "Url": "https://my-service.com/webhook",
    "Enabled": True,
    "SubscribeToAllEvents": False,
    "AllowInsecureSsl": False,
    "Secret": "my-signing-secret",  # Optional
    "Events": [
        "Job.Completed",
        "Job.Faulted"
    ]
})
```

#### Parameters
- `webhook_data` (Dict): Webhook configuration including:
  - `Name` (str, required): Webhook name
  - `Url` (str, required): Webhook endpoint URL
  - `Enabled` (bool, required): Whether webhook is enabled
  - `Events` (List[str], optional): Event types to subscribe to
  - `Secret` (str, optional): Signing secret for payload verification
  - `AllowInsecureSsl` (bool, optional): Allow insecure SSL connections

#### Returns
Dict: Created webhook details

### update()
Update an existing webhook subscription.

```python
client.webhooks.update(123, {
    "Enabled": False,
    "Events": ["Job.Completed"]
})
```

#### Parameters
- `webhook_id` (int): ID of webhook to update
- `webhook_data` (Dict): Updated webhook data

### delete()
Delete a webhook subscription.

```python
client.webhooks.delete(123)
```

#### Parameters
- `webhook_id` (int): ID of webhook to delete

### test()
Test a webhook subscription.

```python
result = client.webhooks.test(123)
```

#### Parameters
- `webhook_id` (int): ID of webhook to test

#### Returns
Dict: Test result details

## Examples

### Webhook Management

```python
def setup_job_monitoring_webhook(url: str, secret: str):
    """Setup webhook for job monitoring"""
    webhook = client.webhooks.create({
        "Name": "JobMonitor",
        "Url": url,
        "Enabled": True,
        "Secret": secret,
        "Events": [
            "Job.Created",
            "Job.Started",
            "Job.Completed",
            "Job.Faulted",
            "Job.Stopped"
        ],
        "Headers": {
            "X-Source": "UiPath",
            "Content-Type": "application/json"
        }
    })
    
    # Test the webhook
    test_result = client.webhooks.test(webhook["Id"])
    
    return {
        "webhook": webhook,
        "test_result": test_result
    }

# Setup job monitoring
result = setup_job_monitoring_webhook(
    url="https://monitor.company.com/webhook",
    secret="secure-secret-key"
)
```

### Event Management

```python
def manage_webhook_events(webhook_id: int, events: Dict[str, bool]):
    """Enable or disable specific webhook events"""
    # Get current webhook config
    webhook = client.webhooks.get_by_id(webhook_id)
    
    # Update events
    current_events = set(webhook["Events"])
    
    for event, enabled in events.items():
        if enabled and event not in current_events:
            current_events.add(event)
        elif not enabled and event in current_events:
            current_events.remove(event)
    
    # Update webhook
    updated = client.webhooks.update(webhook_id, {
        "Events": list(current_events)
    })
    
    return updated

# Manage events
events = {
    "Job.Created": True,
    "Job.Faulted": True,
    "Job.Completed": False
}
updated_webhook = manage_webhook_events(123, events)
```

### Webhook Verification

```python
def verify_webhook_payload(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook payload signature"""
    import hmac
    import hashlib
    
    # Create HMAC SHA256 hash
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(signature, expected)

# Usage in Flask app
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-UiPath-Signature')
    
    if verify_webhook_payload(
        request.get_data(),
        signature,
        "webhook-secret"
    ):
        # Process verified webhook
        return {"status": "success"}, 200
    else:
        return {"status": "invalid signature"}, 401
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to create webhook with invalid URL
    client.webhooks.create({
        "Name": "InvalidWebhook",
        "Url": "invalid-url",
        "Enabled": True
    })
except HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid webhook configuration")
    elif e.response.status_code == 409:
        print("Webhook name already exists")
    else:
        print(f"Error creating webhook: {e}")
```

## Best Practices

1. Use HTTPS endpoints
2. Implement payload verification
3. Handle retries gracefully
4. Monitor webhook health
5. Use descriptive names
6. Subscribe to relevant events
7. Implement proper error handling
8. Regular testing
9. Document webhook integrations

## Security Considerations

1. Use HTTPS endpoints only
2. Implement signature verification
3. Protect webhook secrets
4. Monitor failed deliveries
5. Validate payload data
6. Control webhook access
7. Regular security review

## See Also
- [UiPath Webhooks Documentation](https://docs.uipath.com/orchestrator/docs/about-webhooks)
- [Webhook Security](https://docs.uipath.com/orchestrator/docs/webhook-security)
- [Event Types](https://docs.uipath.com/orchestrator/docs/webhook-event-types)
- [Jobs](jobs.md) for job events
- [Robots](robots.md) for robot events 
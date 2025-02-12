# Queues

The Queues resource allows you to manage UiPath Orchestrator queues and queue items. Queues are used to distribute work items among robots.

## Related Resources
- [Jobs](jobs.md) - Jobs that process queue items
- [Robots](robots.md) - Robots that process queue items
- [Test Data Queue](queues/test_data_queue.md) - Similar functionality for test automation

## Methods

### get()
Get a list of queue definitions.

```python
queues = client.queues.get(name="InvoiceQueue")
```

#### Parameters
- `name` (str, optional): Filter by queue name

#### Returns
List[Dict]: List of queue definitions

### get_by_id()
Get a specific queue definition by ID.

```python
queue = client.queues.get_by_id(123)
```

#### Parameters
- `queue_id` (int): ID of the queue to retrieve

#### Returns
Dict: Queue definition details

### create()
Create a new queue.

```python
queue = client.queues.create({
    "Name": "InvoiceQueue",
    "Description": "Queue for processing invoices",
    "AcceptAutomaticallyRetry": True,
    "MaxNumberOfRetries": 3
})
```

#### Parameters
- `queue_data` (Dict): Queue configuration including:
  - `Name` (str, required): Queue name
  - `Description` (str, optional): Queue description
  - `AcceptAutomaticallyRetry` (bool, optional): Whether to auto-retry failed items
  - `MaxNumberOfRetries` (int, optional): Maximum retry attempts
  - `EnforceUniqueReference` (bool, optional): Enforce unique references

#### Returns
Dict: Created queue details

### add_queue_item()
Add a single item to a queue.

```python
item = client.queues.add_queue_item(
    queue_name="InvoiceQueue",
    item_data={
        "Priority": "High",
        "Reference": "INV-001",
        "SpecificContent": {
            "InvoiceNumber": "001",
            "Amount": 100.00
        }
    }
)
```

#### Parameters
- `queue_name` (str): Name of the queue
- `item_data` (Dict): Item data including:
  - `Priority` (str, optional): Item priority (Low, Normal, High)
  - `Reference` (str, optional): Unique reference
  - `SpecificContent` (Dict): Business data for the item
  - `DeferDate` (str, optional): ISO datetime when item becomes available
  - `DueDate` (str, optional): ISO datetime when item is due

#### Returns
Dict: Created queue item details

### bulk_add_queue_items()
Add multiple items to a queue in one operation.

```python
result = client.queues.bulk_add_queue_items(
    queue_name="InvoiceQueue",
    items=[
        {
            "Priority": "Normal",
            "Reference": "INV-001",
            "SpecificContent": {"InvoiceNumber": "001"}
        },
        {
            "Priority": "High",
            "Reference": "INV-002",
            "SpecificContent": {"InvoiceNumber": "002"}
        }
    ]
)
```

#### Parameters
- `queue_name` (str): Name of the queue
- `items` (List[Dict]): List of item data dictionaries

#### Returns
Dict: Result including number of items added

### get_queue_items()
Get items from a queue with optional filters.

```python
items = client.queues.get_queue_items(
    queue_name="InvoiceQueue",
    status="New"
)
```

#### Parameters
- `queue_name` (str, optional): Filter by queue name
- `status` (str, optional): Filter by status. Valid values:
  - `New`
  - `InProgress`
  - `Failed`
  - `Successful`
  - `Retried`
  - `Abandoned`

#### Returns
List[Dict]: List of queue items matching filters

### set_transaction_status()
Update the status of a queue item.

```python
client.queues.set_transaction_status(
    queue_item_id=123,
    status="Successful",
    reason="Processing completed successfully"
)
```

#### Parameters
- `queue_item_id` (int): ID of the queue item
- `status` (str): New status (Success, Failed, Retried)
- `
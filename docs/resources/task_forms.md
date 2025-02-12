# Task Forms

The Task Forms resource allows you to manage UiPath Task Forms, which enable human interaction within automation processes. Task Forms can collect user input, display information, and facilitate decision-making.

## Related Resources
- [Jobs](jobs.md) - Jobs that use task forms
- [Processes](processes.md) - Processes that include forms
- [Robots](robots.md) - Robots that interact with forms

## Methods

### get()
Get a list of task forms with optional filters.

```python
forms = client.task_forms.get(
    process_name="InvoiceProcess",    # Filter by process
    status="Pending"                  # Filter by status
)
```

#### Parameters
- `process_name` (str, optional): Filter by process name
- `status` (str, optional): Filter by form status (Pending, Completed, Canceled)

#### Returns
List[Dict]: List of task form objects matching the filters

### get_by_id()
Get a specific task form by ID.

```python
form = client.task_forms.get_by_id(123)
```

#### Parameters
- `form_id` (int): ID of the form to retrieve

#### Returns
Dict: Task form details

### submit()
Submit a response to a task form.

```python
client.task_forms.submit(
    form_id=123,
    data={
        "approved": True,
        "comments": "Invoice approved for payment"
    }
)
```

#### Parameters
- `form_id` (int): ID of the form to submit
- `data` (Dict): Form response data

### assign()
Assign a task form to a user.

```python
client.task_forms.assign(
    form_id=123,
    user_id=456
)
```

#### Parameters
- `form_id` (int): ID of the form
- `user_id` (int): ID of the user to assign

## Examples

### Form Processing

```python
def process_approval_forms(process_name: str):
    """Process pending approval forms"""
    # Get pending forms
    forms = client.task_forms.get(
        process_name=process_name,
        status="Pending"
    )
    
    results = []
    for form in forms:
        try:
            # Process form based on type
            if form["FormType"] == "ApprovalForm":
                # Get form data
                data = form["Data"]
                
                # Make approval decision
                approved = data["Amount"] <= 1000
                
                # Submit response
                client.task_forms.submit(
                    form_id=form["Id"],
                    data={
                        "approved": approved,
                        "comments": "Auto-processed based on amount",
                        "processedAt": datetime.now().isoformat()
                    }
                )
                
                results.append({
                    "form_id": form["Id"],
                    "status": "processed",
                    "approved": approved
                })
                
        except Exception as e:
            results.append({
                "form_id": form["Id"],
                "status": "error",
                "error": str(e)
            })
    
    return results

# Process approval forms
results = process_approval_forms("InvoiceApproval")
```

### Form Assignment

```python
def assign_forms_to_team(team_forms: List[Dict]):
    """Assign forms to team members"""
    for assignment in team_forms:
        try:
            client.task_forms.assign(
                form_id=assignment["form_id"],
                user_id=assignment["user_id"]
            )
            
            # Add assignment metadata
            client.task_forms.update(
                form_id=assignment["form_id"],
                metadata={
                    "assigned_by": "auto_assignment",
                    "assigned_at": datetime.now().isoformat(),
                    "priority": assignment.get("priority", "normal")
                }
            )
            
        except Exception as e:
            print(f"Error assigning form {assignment['form_id']}: {e}")

# Assign forms
assignments = [
    {"form_id": 123, "user_id": 456, "priority": "high"},
    {"form_id": 124, "user_id": 457, "priority": "normal"}
]
assign_forms_to_team(assignments)
```

### Form Monitoring

```python
def monitor_form_sla(sla_minutes: int = 60):
    """Monitor forms for SLA compliance"""
    forms = client.task_forms.get(status="Pending")
    
    violations = []
    for form in forms:
        created_time = datetime.fromisoformat(form["CreatedTime"])
        elapsed_minutes = (datetime.now() - created_time).total_seconds() / 60
        
        if elapsed_minutes > sla_minutes:
            violations.append({
                "form_id": form["Id"],
                "process": form["ProcessName"],
                "elapsed_minutes": elapsed_minutes,
                "assigned_to": form.get("AssignedTo")
            })
    
    return violations

# Check SLA violations
violations = monitor_form_sla(sla_minutes=30)
```

### Bulk Form Operations

```python
def bulk_form_operations(operation: str, form_ids: List[int], **kwargs):
    """Perform bulk operations on forms"""
    results = []
    
    for form_id in form_ids:
        try:
            if operation == "cancel":
                client.task_forms.cancel(
                    form_id=form_id,
                    reason=kwargs.get("reason", "Bulk cancellation")
                )
            elif operation == "reassign":
                client.task_forms.assign(
                    form_id=form_id,
                    user_id=kwargs["user_id"]
                )
            elif operation == "update_priority":
                client.task_forms.update(
                    form_id=form_id,
                    metadata={"priority": kwargs["priority"]}
                )
                
            results.append({
                "form_id": form_id,
                "status": "success",
                "operation": operation
            })
            
        except Exception as e:
            results.append({
                "form_id": form_id,
                "status": "error",
                "operation": operation,
                "error": str(e)
            })
    
    return results

# Perform bulk operations
form_ids = [123, 124, 125]
results = bulk_form_operations("reassign", form_ids, user_id=789)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to submit to completed form
    client.task_forms.submit(
        form_id=123,
        data={"approved": True}
    )
except HTTPError as e:
    if e.response.status_code == 400:
        print("Form already completed or invalid")
    elif e.response.status_code == 404:
        print("Form not found")
    else:
        print(f"Error submitting form: {e}")
```

## Best Practices

1. Set appropriate form timeouts
2. Implement form validation
3. Monitor form completion times
4. Document form requirements
5. Regular SLA monitoring
6. Clear error messages
7. Audit form submissions
8. Backup form data
9. Test form workflows

## Security Considerations

1. Validate form inputs
2. Control form access
3. Audit form changes
4. Secure sensitive data
5. Monitor form usage
6. Implement timeouts
7. Version control forms

## See Also
- [UiPath Forms Documentation](https://docs.uipath.com/orchestrator/docs/about-forms)
- [Form Design Guide](https://docs.uipath.com/orchestrator/docs/designing-forms)
- [Form Security](https://docs.uipath.com/orchestrator/docs/form-security)
- [Jobs](jobs.md) for process execution
- [Processes](processes.md) for workflow management 
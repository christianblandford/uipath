# UiPath Python SDK

A Python SDK for interacting with the UiPath Orchestrator API.

## Features

- Complete API coverage for UiPath Orchestrator
- Easy-to-use interface
- Type hints for better IDE support
- Comprehensive documentation
- Examples for common use cases

## Installation 

```bash
pip install uipath
```

## Quick Start

```python
from uipath import UiPathClient

client = UiPathClient(
    organization_id="your_organization_id",
    tenant_id="your_tenant_id",
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```
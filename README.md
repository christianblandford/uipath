# 🤖 UiPath Python SDK

The most awesome Python SDK for UiPath Orchestrator! Automate all the things with simple Python code. 

[![PyPI version](https://badge.fury.io/py/uipath.svg)](https://badge.fury.io/py/uipath)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://christianblandford.github.io/uipath/)

## 🚀 Quick Install

```bash
pip install uipath
```

## ⚡ Quick Start

```python
from uipath import UiPathClient

# Connect to UiPath in just 3 lines! 🎉
client = UiPathClient(
    organization_id="your_organization_id",
    tenant_id="your_tenant_id", 
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

## 🎯 Why Choose This SDK?

- 📚 **Amazing Docs** - [Check them out here!](https://christianblandford.github.io/uipath/)
- 🔥 **Complete API Coverage** - Access everything UiPath Orchestrator offers
- 🎈 **Super Simple Interface** - Designed for humans, by humans
- 🛡️ **Type Hints** - Get awesome IDE support

## 🎨 Features

Manage all your UiPath resources with Python:

- 🤖 Robots
- 📦 Packages
- 📋 Jobs
- 📁 Folders
- 🎮 Processes
- 🔑 Assets
- 📥 Queues
- 📚 Libraries
- 💻 Machines
- ...and more!

## 📖 Examples

### Managing Robots

```python
# List all your robot friends
robots = client.robots.get_all()

# Create a new robot buddy
new_robot = client.robots.create({
    "Name": "Wall-E",
    "Type": "Unattended",
    "Username": "domain\\wall-e"
})

# Update robot status
client.robots.toggle_enabled(robot_id=123, enabled=True)
```

### Working with Queues

```python
# Add items to your queue
client.queues.add_queue_item(
    queue_name="TPS_Reports",
    reference="TPS-001",
    priority="High",
    specific_content={
        "ReportNumber": "TPS-001",
        "Urgent": True
    }
)

# Process queue items
items = client.queues.get_queue_items(
    queue_name="TPS_Reports",
    status="New"
)
```

## 🔧 Configuration

```python
client = UiPathClient(
    organization_id="org_id",
    tenant_id="tenant_id",
    client_id="client_id",
    client_secret="shhh_its_a_secret",
    base_url="https://cloud.uipath.com"  # Optional
)
```

## 📚 Documentation

For full documentation, visit our [awesome docs page](https://christianblandford.github.io/uipath/)!

## 🤝 Contributing

We love contributions! Here's how:

1. 🍴 Fork it
2. 🌱 Create your feature branch (`git checkout -b feature/CoolFeature`)
3. 💾 Commit your changes (`git commit -m 'Add CoolFeature'`)
4. 📤 Push to the branch (`git push origin feature/CoolFeature`)
5. 🎁 Open a Pull Request

## 📝 License

MIT License - go wild! See [LICENSE](LICENSE) for more details.

## 💪 Support

Need help? We've got your back!

1. 📚 [Check out our docs](https://christianblandford.github.io/uipath/)
2. 🎫 [Open an issue](https://github.com/christianblandford/uipath/issues)
3. 💬 [Start a discussion](https://github.com/christianblandford/uipath/discussions)

## ⚡ Requirements

- Python 3.7+
- A love for automation! 🤖

## 📢 Disclaimer

This is an unofficial SDK created with ❤️ by the community. Not affiliated with UiPath Inc.

---
Made with 🦾 by developers, for developers

# Settings

The Settings resource allows you to manage UiPath Orchestrator configuration settings, including system preferences, default values, and feature toggles.

## Related Resources
- [Status](status.md) - System status affected by settings
- [Maintenance](settings/maintenance.md) - System maintenance configuration
- [Directory](directory.md) - User and authentication settings

## Methods

### get_settings()
Get current system settings.

```python
settings = client.settings.get_settings()
```

#### Returns
Dict: Current system settings including:
- Authentication settings
- Email configuration
- Performance settings
- Feature flags
- Default values

### update_settings()
Update system settings.

```python
client.settings.update_settings({
    "SmtpSettings": {
        "Host": "smtp.company.com",
        "Port": 587,
        "EnableSsl": True
    },
    "AuthenticationSettings": {
        "LoginTimeout": 30,
        "MaxLoginAttempts": 5
    }
})
```

#### Parameters
- `settings` (Dict): Settings to update

### get_feature_flags()
Get status of feature flags.

```python
flags = client.settings.get_feature_flags()
```

#### Returns
Dict: Feature flag states

### update_feature_flag()
Update a feature flag setting.

```python
client.settings.update_feature_flag(
    flag_name="NewFeature",
    enabled=True
)
```

#### Parameters
- `flag_name` (str): Name of the feature flag
- `enabled` (bool): Whether to enable the feature

## Examples

### Email Configuration

```python
def configure_email_settings(config: Dict):
    """Configure system email settings"""
    try:
        # Update SMTP settings
        client.settings.update_settings({
            "SmtpSettings": {
                "Host": config["host"],
                "Port": config["port"],
                "EnableSsl": config["ssl"],
                "Username": config["username"],
                "Password": config["password"],
                "FromAddress": config["from_address"],
                "UseDefaultCredentials": False
            }
        })
        
        # Test configuration
        test_result = client.settings.test_email_settings()
        
        return {
            "success": test_result["Success"],
            "message": test_result.get("Message", "Settings updated")
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

# Configure email
email_config = {
    "host": "smtp.company.com",
    "port": 587,
    "ssl": True,
    "username": "notifications@company.com",
    "password": "secure_password",
    "from_address": "uipath@company.com"
}
result = configure_email_settings(email_config)
```

### Authentication Settings

```python
def configure_authentication(settings: Dict):
    """Configure authentication settings"""
    auth_settings = {
        "AuthenticationSettings": {
            "LoginTimeout": settings["timeout"],
            "MaxLoginAttempts": settings["max_attempts"],
            "LockoutDuration": settings["lockout_minutes"],
            "RequireMfa": settings["require_mfa"],
            "PasswordPolicy": {
                "MinLength": settings["min_password_length"],
                "RequireUppercase": True,
                "RequireLowercase": True,
                "RequireDigit": True,
                "RequireSpecialCharacter": True
            }
        }
    }
    
    return client.settings.update_settings(auth_settings)

# Configure authentication
auth_config = {
    "timeout": 30,
    "max_attempts": 5,
    "lockout_minutes": 15,
    "require_mfa": True,
    "min_password_length": 12
}
configure_authentication(auth_config)
```

### Feature Management

```python
def manage_features(environment: str):
    """Manage feature flags based on environment"""
    # Get current flags
    flags = client.settings.get_feature_flags()
    
    # Define environment-specific features
    env_features = {
        "development": {
            "NewFeature": True,
            "BetaFeature": True,
            "ExperimentalApi": True
        },
        "production": {
            "NewFeature": False,
            "BetaFeature": False,
            "ExperimentalApi": False
        }
    }
    
    # Update flags
    updates = []
    for flag, enabled in env_features[environment].items():
        try:
            client.settings.update_feature_flag(
                flag_name=flag,
                enabled=enabled
            )
            updates.append({
                "flag": flag,
                "status": "updated",
                "enabled": enabled
            })
        except Exception as e:
            updates.append({
                "flag": flag,
                "status": "error",
                "error": str(e)
            })
    
    return updates

# Manage features for environment
updates = manage_features("development")
```

### Performance Settings

```python
def optimize_performance_settings(load_profile: str):
    """Optimize system settings for different load profiles"""
    profiles = {
        "light": {
            "MaxConcurrentJobs": 10,
            "JobExpirationDays": 30,
            "LogRetentionDays": 90,
            "QueueRetentionDays": 30
        },
        "medium": {
            "MaxConcurrentJobs": 50,
            "JobExpirationDays": 15,
            "LogRetentionDays": 60,
            "QueueRetentionDays": 15
        },
        "heavy": {
            "MaxConcurrentJobs": 100,
            "JobExpirationDays": 7,
            "LogRetentionDays": 30,
            "QueueRetentionDays": 7
        }
    }
    
    settings = profiles[load_profile]
    return client.settings.update_settings({
        "PerformanceSettings": settings
    })

# Optimize for load
optimize_performance_settings("medium")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    # Try to update sensitive settings
    client.settings.update_settings({
        "SecuritySettings": {
            "EnabledCiphers": ["TLS_1_2"]
        }
    })
except HTTPError as e:
    if e.response.status_code == 403:
        print("Insufficient permissions")
    elif e.response.status_code == 400:
        print("Invalid settings configuration")
    else:
        print(f"Error updating settings: {e}")
```

## Best Practices

1. Document settings changes
2. Test in non-production first
3. Use environment-specific configs
4. Regular settings review
5. Backup settings before changes
6. Monitor impact of changes
7. Maintain settings history
8. Validate configurations
9. Control settings access

## Security Considerations

1. Restrict settings access
2. Audit settings changes
3. Secure sensitive settings
4. Regular security review
5. Validate setting values
6. Monitor configuration changes
7. Document security settings

## See Also
- [UiPath Settings Documentation](https://docs.uipath.com/orchestrator/docs/managing-settings)
- [Security Configuration](https://docs.uipath.com/orchestrator/docs/security-configuration)
- [Performance Tuning](https://docs.uipath.com/orchestrator/docs/performance-tuning)
- [Status](status.md) for system monitoring
- [Maintenance](settings/maintenance.md) for system maintenance 
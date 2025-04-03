from typing import Optional, Dict, List
from ..base_client import BaseClient

class SettingsClient:
    def __init__(self, client: BaseClient):
        self._client = client

    def get_settings(self) -> Dict:
        """
        Get current system settings.
        
        Returns:
            Dict: Current system settings including:
            - Authentication settings
            - Email configuration
            - Performance settings
            - Feature flags
            - Default values
        """
        return self._client._make_request('GET', '/odata/Settings')

    def update_settings(self, settings: Dict) -> Dict:
        """
        Update system settings.
        
        Args:
            settings: Dict containing settings to update, which may include:
                - SmtpSettings: Email server configuration
                - AuthenticationSettings: Authentication configuration
                - PerformanceSettings: Performance tuning settings
                - SecuritySettings: Security configuration
                
        Returns:
            Dict: Updated settings
        """
        return self._client._make_request(
            'PUT',
            '/odata/Settings',
            json=settings
        )

    def get_feature_flags(self) -> Dict:
        """
        Get status of feature flags.
        
        Returns:
            Dict: Feature flags and their current states
        """
        return self._client._make_request('GET', '/odata/Settings/FeatureFlags')

    def update_feature_flags(self, flags: Dict) -> Dict:
        """
        Update feature flag settings.
        
        Args:
            flags: Dict of feature flags to update
            
        Returns:
            Dict: Updated feature flags
        """
        return self._client._make_request(
            'PUT',
            '/odata/Settings/FeatureFlags',
            json=flags
        )

    def get_license_settings(self) -> Dict:
        """
        Get license-related settings.
        
        Returns:
            Dict: License settings and configuration
        """
        return self._client._make_request('GET', '/odata/Settings/License')

    def get_authentication_settings(self) -> Dict:
        """
        Get authentication settings.
        
        Returns:
            Dict: Authentication configuration settings
        """
        return self._client._make_request('GET', '/odata/Settings/Authentication')

    def update_authentication_settings(self, settings: Dict) -> Dict:
        """
        Update authentication settings.
        
        Args:
            settings: Authentication settings to update
            
        Returns:
            Dict: Updated authentication settings
        """
        return self._client._make_request(
            'PUT',
            '/odata/Settings/Authentication',
            json=settings
        ) 
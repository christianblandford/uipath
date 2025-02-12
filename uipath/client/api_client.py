import requests
from typing import Optional, Dict, List, Any
from ..auth.authentication import UiPathAuth
from .resources.assets import AssetsClient
from .resources.queues import QueuesClient
from .resources.jobs import JobsClient
from .resources.folders import FoldersClient
from .resources.releases import ReleasesClient
from .base_client import BaseClient
from .resources.packages import PackagesClient
from .resources.libraries import LibrariesClient
from .resources.machines import MachinesClient
from .resources.processes import ProcessesClient
from .resources.robots import RobotsClient
from .resources.directory import DirectoryClient
from .resources.maintenance import MaintenanceClient
from .resources.stats import StatsClient
from .resources.status import StatusClient
from .resources.test_automation import TestAutomationClient
from .resources.test_data_queue import TestDataQueueClient
from .resources.webhooks import WebhooksClient
from .resources.licensing import LicensingClient
from .resources.logs import LogsClient
from .resources.task_forms import TaskFormsClient
from .resources.alerts import AlertsClient
from .resources.audit import AuditClient
from .resources.environments import EnvironmentsClient
from .resources.metrics import MetricsClient
from .resources.settings import SettingsClient
from .resources.users import UsersClient

class UiPathClient(BaseClient):
    def __init__(
        self,
        auth: UiPathAuth,
        base_url: str = "https://cloud.uipath.com"
    ):
        super().__init__(auth, base_url)
        
        # Initialize all resource clients
        self.alerts = AlertsClient(self)
        self.assets = AssetsClient(self)
        self.audit = AuditClient(self)
        self.directory = DirectoryClient(self)
        self.environments = EnvironmentsClient(self)
        self.folders = FoldersClient(self)
        self.jobs = JobsClient(self)
        self.libraries = LibrariesClient(self)
        self.logs = LogsClient(self)
        self.machines = MachinesClient(self)
        self.maintenance = MaintenanceClient(self)
        self.metrics = MetricsClient(self)
        self.packages = PackagesClient(self)
        self.processes = ProcessesClient(self)
        self.queues = QueuesClient(self)
        self.releases = ReleasesClient(self)
        self.robots = RobotsClient(self)
        self.settings = SettingsClient(self)
        self.stats = StatsClient(self)
        self.task_forms = TaskFormsClient(self)
        self.users = UsersClient(self)
        self.webhooks = WebhooksClient(self)
        self.test_automation = TestAutomationClient(self)
        self.test_data_queue = TestDataQueueClient(self)
        self.licensing = LicensingClient(self)

    def _make_request(
        self, 
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Any:
        """Make HTTP request to UiPath API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.auth.get_headers()
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json
        )
        response.raise_for_status()
        
        if response.content:
            return response.json()
        return None

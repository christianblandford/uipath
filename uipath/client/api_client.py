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

class UiPathClient(BaseClient):
    def __init__(
        self,
        auth: UiPathAuth,
        base_url: str = "https://cloud.uipath.com"
    ):
        super().__init__(auth, base_url)
        
        # Initialize resource clients
        self.assets = AssetsClient(self)
        self.queues = QueuesClient(self)
        self.jobs = JobsClient(self)
        self.folders = FoldersClient(self)
        self.releases = ReleasesClient(self)
        self.packages = PackagesClient(self)
        self.libraries = LibrariesClient(self)
        self.machines = MachinesClient(self)
        self.processes = ProcessesClient(self)
        self.robots = RobotsClient(self)

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

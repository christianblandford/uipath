from typing import Optional, Dict, List
from ..base_client import BaseClient

class TestAutomationClient:
    """Client for managing UiPath Test Automation"""
    
    def __init__(self, client: BaseClient):
        self._client = client

    def cancel_test_case_execution(self, test_case_execution_id: int) -> None:
        """
        Cancels the specified test case execution.
        
        Args:
            test_case_execution_id: Id for the test case execution to be canceled
        """
        params = {"testCaseExecutionId": test_case_execution_id}
        self._client._make_request(
            'POST',
            '/api/TestAutomation/CancelTestCaseExecution',
            params=params
        )

    def cancel_test_set_execution(self, test_set_execution_id: int) -> None:
        """
        Cancels the specified test set execution.
        
        Args:
            test_set_execution_id: Id for the test set execution to be canceled
        """
        params = {"testSetExecutionId": test_set_execution_id}
        self._client._make_request(
            'POST',
            '/api/TestAutomation/CancelTestSetExecution',
            params=params
        )

    def create_test_set(self, test_set_data: Dict) -> int:
        """
        Creates a test set with source type API.
        
        Args:
            test_set_data: Test set configuration data
            
        Returns:
            Created test set ID
        """
        response = self._client._make_request(
            'POST',
            '/api/TestAutomation/CreateTestSetForReleaseVersion',
            json=test_set_data
        )
        return response

    def get_assertion_screenshot(self, test_case_assertion_id: int) -> bytes:
        """
        Get the screenshot for the specified test case assertion.
        
        Args:
            test_case_assertion_id: Id of the test case assertion
            
        Returns:
            Screenshot data as bytes
        """
        return self._client._make_request(
            'GET',
            '/api/TestAutomation/GetAssertionScreenshot',
            params={"testCaseAssertionId": test_case_assertion_id}
        )

    def get_package_info(self, test_case_unique_id: str, package_identifier: str) -> Dict:
        """
        Get package info for a test case.
        
        Args:
            test_case_unique_id: Test case unique identifier
            package_identifier: Package identifier
            
        Returns:
            Package information
        """
        params = {
            "testCaseUniqueId": test_case_unique_id,
            "packageIdentifier": package_identifier
        }
        return self._client._make_request(
            'GET',
            '/api/TestAutomation/GetPackageInfoByTestCaseUniqueId',
            params=params
        )

    def start_test_set_execution(
        self,
        test_set_id: Optional[int] = None,
        test_set_key: Optional[str] = None,
        trigger_type: str = "Manual"
    ) -> int:
        """
        Start a test set execution.
        
        Args:
            test_set_id: Test set ID
            test_set_key: Test set key
            trigger_type: How execution was triggered (Manual, Scheduled, etc)
            
        Returns:
            Test set execution ID
        """
        params = {"triggerType": trigger_type}
        if test_set_id:
            params["testSetId"] = test_set_id
        if test_set_key:
            params["testSetKey"] = test_set_key
            
        return self._client._make_request(
            'POST',
            '/api/TestAutomation/StartTestSetExecution',
            params=params
        ) 
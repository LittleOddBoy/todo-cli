import requests
from typing import Dict, Optional, List
from .config import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"API Error: {str(e)}")
            raise
        return response.json()

    def get_tasks(self) -> List[Dict]:
        """Get all tasks"""
        response = requests.get(f"{self.base_url}/tasks", headers=self.headers)
        return self._handle_response(response)

    def get_task(self, task_id: str) -> Dict:
        """Get a single task by ID"""
        response = requests.get(f"{self.base_url}/tasks/{task_id}", headers=self.headers)
        return self._handle_response(response)

    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        response = requests.post(
            f"{self.base_url}/tasks",
            json=task_data,
            headers=self.headers
        )
        return self._handle_response(response)

    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        """Update an existing task"""
        response = requests.put(
            f"{self.base_url}/tasks/{task_id}",
            json=task_data,
            headers=self.headers
        )
        return self._handle_response(response)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        response = requests.delete(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        return response.status_code == 204

    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task with better error handling"""
        try:
            response = requests.post(
                f"{self.base_url}/tasks",
                json=task_data,
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Request failed: {str(e)}"
            if hasattr(e, "response") and e.response.text:
                error_message += f"\nServer response: {e.response.text[:200]}"
            raise Exception(error_message)
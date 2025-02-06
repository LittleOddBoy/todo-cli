from typing import Dict, Optional, List
from .config import settings
from .auth import AuthHandler
import random

class MockAPIClient:
    def __init__(self):
        self.auth = AuthHandler()
        self.storage = []
        
    # Authentication methods
    def signup(self, user_data: Dict) -> Dict:
        return {"message": "User created", "token": "mock_token", "user_id": "123"}
        
    def login(self, credentials: Dict) -> Dict:
        return {"message": "Login successful", "token": "mock_token", "user_id": "123"}
    
    # Task methods
    def get_tasks(self) -> List[Dict]:
        return self.storage
    
    def create_task(self, task_data: Dict) -> Dict:
        task_id = str(random.randint(1000, 9999))
        task = {"id": task_id, **task_data}
        self.storage.append(task)
        return {"id": task_id, "message": "Task created"}
    
    def delete_task(self, task_id: str) -> bool:
        self.storage = [t for t in self.storage if t["id"] != task_id]
        return True
    
    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        for task in self.storage:
            if task["id"] == task_id:
                task.update(task_data)
                return {"message": "Task updated"}
        return {"error": "Task not found"}
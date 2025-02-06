import json
import os
from appdirs import user_config_dir
from typing import Optional

class AuthHandler:
    def __init__(self):
        self.config_dir = user_config_dir("todo-cli")
        self.auth_file = os.path.join(self.config_dir, "auth.json")
        os.makedirs(self.config_dir, exist_ok=True)

    def save_auth_token(self, token: str, user_id: str):
        """Save authentication token securely"""
        data = {"token": token, "user_id": user_id}
        with open(self.auth_file, "w") as f:
            json.dump(data, f)
        os.chmod(self.auth_file, 0o600)  # Secure file permissions

    def get_auth_token(self) -> Optional[dict]:
        """Retrieve stored authentication token"""
        try:
            with open(self.auth_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def clear_auth(self):
        """Remove authentication credentials"""
        try:
            os.remove(self.auth_file)
        except FileNotFoundError:
            pass
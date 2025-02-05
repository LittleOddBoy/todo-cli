from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    title: str
    description: Optional[str] = None
    completed: bool = False

    def validate(self):
        """Basic validation logic"""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title too long (max 200 characters)")
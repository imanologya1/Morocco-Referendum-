"""
Poll model for database
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import uuid


class Poll:
    """Represents a voting poll"""
    
    def __init__(self, poll_id: str = None, title: str = "", question: str = "",
                 options: List[str] = None, creator: str = "", duration_hours: int = 24,
                 language: str = "en", created_at: float = None, closes_at: float = None,
                 status: str = "active", public_key: str = "", private_key: str = ""):
        self.poll_id = poll_id or str(uuid.uuid4())
        self.title = title
        self.question = question
        self.options = options or []
        self.creator = creator
        self.duration_hours = duration_hours
        self.language = language
        self.created_at = created_at or datetime.now().timestamp()
        self.closes_at = closes_at or (self.created_at + duration_hours * 3600)
        self.status = status  # active, closed, counting
        self.public_key = public_key
        self.private_key = private_key
        self.results: Optional[Dict[str, int]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert poll to dictionary"""
        return {
            "poll_id": self.poll_id,
            "title": self.title,
            "question": self.question,
            "options": self.options,
            "creator": self.creator,
            "duration_hours": self.duration_hours,
            "language": self.language,
            "created_at": self.created_at,
            "closes_at": self.closes_at,
            "status": self.status,
            "public_key": self.public_key,
            "private_key": self.private_key if self.status == "closed" else "",
            "results": self.results
        }
    
    def to_public_dict(self) -> Dict[str, Any]:
        """Convert poll to public dictionary (without private key)"""
        data = self.to_dict()
        data["private_key"] = ""  # Never expose private key until closed
        return data
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Poll':
        """Create poll from dictionary"""
        poll = Poll(
            poll_id=data.get("poll_id"),
            title=data.get("title", ""),
            question=data.get("question", ""),
            options=data.get("options", []),
            creator=data.get("creator", ""),
            duration_hours=data.get("duration_hours", 24),
            language=data.get("language", "en"),
            created_at=data.get("created_at"),
            closes_at=data.get("closes_at"),
            status=data.get("status", "active"),
            public_key=data.get("public_key", ""),
            private_key=data.get("private_key", "")
        )
        poll.results = data.get("results")
        return poll
    
    def is_active(self) -> bool:
        """Check if poll is still active"""
        return self.status == "active" and datetime.now().timestamp() < self.closes_at
    
    def close(self):
        """Close the poll"""
        self.status = "closed"
    
    def set_results(self, results: Dict[str, int]):
        """Set poll results after counting"""
        self.results = results


class PollStore:
    """Simple file-based storage for polls"""
    
    def __init__(self, storage_file: str = "polls.json"):
        self.storage_file = storage_file
        self.polls: Dict[str, Poll] = {}
        self.load_polls()
    
    def load_polls(self):
        """Load polls from file"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.polls = {
                    poll_id: Poll.from_dict(poll_data)
                    for poll_id, poll_data in data.items()
                }
        except (FileNotFoundError, json.JSONDecodeError):
            self.polls = {}
            self.save_polls()
    
    def save_polls(self):
        """Save polls to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(
                {poll_id: poll.to_dict() for poll_id, poll in self.polls.items()},
                f,
                indent=2
            )
    
    def create_poll(self, poll: Poll) -> Poll:
        """Create a new poll"""
        self.polls[poll.poll_id] = poll
        self.save_polls()
        return poll
    
    def get_poll(self, poll_id: str) -> Optional[Poll]:
        """Get a poll by ID"""
        return self.polls.get(poll_id)
    
    def update_poll(self, poll: Poll):
        """Update an existing poll"""
        self.polls[poll.poll_id] = poll
        self.save_polls()
    
    def get_all_polls(self) -> List[Poll]:
        """Get all polls"""
        return list(self.polls.values())
    
    def get_active_polls(self) -> List[Poll]:
        """Get all active polls"""
        return [poll for poll in self.polls.values() if poll.is_active()]
    
    def delete_poll(self, poll_id: str) -> bool:
        """Delete a poll"""
        if poll_id in self.polls:
            del self.polls[poll_id]
            self.save_polls()
            return True
        return False

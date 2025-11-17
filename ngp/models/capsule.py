"""Time Capsule model - letters to future self"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class UnlockType(Enum):
    """Ways a time capsule can unlock"""
    DATE = "date"
    MISSION_COMPLETION = "mission_completion"
    SKILL_LEVEL = "skill_level"
    PLAYER_LEVEL = "player_level"


@dataclass
class TimeCapsule:
    """
    Represents a time capsule - a letter to your future self.

    Attributes:
        id: Unique identifier
        title: Capsule title
        body: Capsule content (letter)
        created_at: When capsule was created
        is_encrypted: Whether content is encrypted
        passphrase_hint: Optional hint for passphrase
        unlock_type: How this capsule unlocks
        unlock_params: Parameters for unlock condition
        unlocked_at: When capsule was unlocked
        archived_to_journal_entry_id: If archived to journal, the entry ID
    """
    id: str
    title: str
    body: str
    unlock_type: UnlockType
    unlock_params: Dict[str, Any]  # e.g., {"date": "2025-12-31"} or {"skill_id": "...", "level": 10}
    created_at: datetime = field(default_factory=datetime.now)
    is_encrypted: bool = False
    passphrase_hint: Optional[str] = None
    unlocked_at: Optional[datetime] = None
    archived_to_journal_entry_id: Optional[str] = None

    def is_unlocked(self) -> bool:
        """Check if capsule has been unlocked"""
        return self.unlocked_at is not None

    def unlock(self):
        """Mark capsule as unlocked"""
        if not self.is_unlocked():
            self.unlocked_at = datetime.now()

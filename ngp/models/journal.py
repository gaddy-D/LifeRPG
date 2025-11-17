"""Journal model - for reflections and notes"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class JournalEntry:
    """
    Represents a journal entry or reflection.

    Attributes:
        id: Unique identifier
        created_at: When entry was created
        text: Entry content
        skill_id: Optional linked skill
        mission_id: Optional linked mission
        is_reflection_token: Whether this was a prompted reflection
        edited_at: When entry was last edited
    """
    id: str
    text: str
    created_at: datetime = field(default_factory=datetime.now)
    skill_id: Optional[str] = None
    mission_id: Optional[str] = None
    is_reflection_token: bool = False
    edited_at: Optional[datetime] = None

    def update(self, new_text: str):
        """Update entry text and set edited timestamp"""
        self.text = new_text
        self.edited_at = datetime.now()

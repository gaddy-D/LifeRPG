"""
Reflection Loop - Journaling and reflection prompts.

[Action Loop]
      ↓
[Reflection Loop] → (Journals, Reflections)
      ↓
[Analysis Loop]
"""

import uuid
import random
from datetime import datetime, timedelta
from typing import Optional, List
from ..models import JournalEntry, Completion
from ..services import StorageService


class ReflectionLoop:
    """
    Manages reflection prompts and journal entries.
    Implements rate-limited reflection tokens to avoid farming.
    """

    # Reflection prompts
    PROMPTS = [
        "What did you learn from this?",
        "How did this make you feel?",
        "What would you do differently next time?",
        "What surprised you about this?",
        "What's one thing you're proud of here?",
        "How does this connect to your larger goals?",
        "What challenge did you overcome?",
        "What skill did you practice?",
        "What would you tell your past self about this?",
        "What's your next step from here?"
    ]

    def __init__(self, storage: StorageService):
        self.storage = storage
        self.reflection_probability = 0.10  # 10% chance
        self.max_daily_reflections = 2
        self.max_skill_cycle_reflections = 7

    def should_prompt_reflection(
        self,
        completion: Completion,
        skill_id: Optional[str] = None
    ) -> bool:
        """
        Determine if we should prompt for a reflection.
        Rate-limited: ~10% chance, max 2/day, max 7/skill-cycle.

        Args:
            completion: The completion that just happened
            skill_id: Optional skill ID for cycle-based limiting

        Returns:
            True if we should show reflection prompt
        """
        # Roll for 10% chance
        if random.random() > self.reflection_probability:
            return False

        # Check daily limit
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_reflections = self._count_reflections_since(today_start)
        if today_reflections >= self.max_daily_reflections:
            return False

        # Check skill-cycle limit if skill provided
        if skill_id:
            cycle_reflections = self._count_skill_cycle_reflections(
                skill_id, completion.cycle_id
            )
            if cycle_reflections >= self.max_skill_cycle_reflections:
                return False

        return True

    def get_random_prompt(self) -> str:
        """Get a random reflection prompt"""
        return random.choice(self.PROMPTS)

    def create_reflection(
        self,
        text: str,
        mission_id: Optional[str] = None,
        skill_id: Optional[str] = None
    ) -> JournalEntry:
        """
        Create a reflection journal entry.

        Args:
            text: Reflection text
            mission_id: Optional linked mission
            skill_id: Optional linked skill

        Returns:
            Created JournalEntry
        """
        entry = JournalEntry(
            id=str(uuid.uuid4()),
            text=text,
            mission_id=mission_id,
            skill_id=skill_id,
            is_reflection_token=True
        )

        self.storage.save_journal_entry(entry)
        return entry

    def create_journal_entry(
        self,
        text: str,
        mission_id: Optional[str] = None,
        skill_id: Optional[str] = None
    ) -> JournalEntry:
        """
        Create a freeform journal entry (not a reflection token).

        Args:
            text: Journal text
            mission_id: Optional linked mission
            skill_id: Optional linked skill

        Returns:
            Created JournalEntry
        """
        entry = JournalEntry(
            id=str(uuid.uuid4()),
            text=text,
            mission_id=mission_id,
            skill_id=skill_id,
            is_reflection_token=False
        )

        self.storage.save_journal_entry(entry)
        return entry

    def get_recent_entries(self, limit: int = 20) -> List[JournalEntry]:
        """Get recent journal entries"""
        return self.storage.get_journal_entries(limit=limit)

    def get_reflections_only(self, limit: int = 20) -> List[JournalEntry]:
        """Get only reflection token entries"""
        entries = self.storage.get_journal_entries(limit=limit * 2)
        reflections = [e for e in entries if e.is_reflection_token]
        return reflections[:limit]

    def _count_reflections_since(self, since: datetime) -> int:
        """Count reflections since a given time"""
        entries = self.storage.get_journal_entries(limit=100)
        return sum(
            1 for e in entries
            if e.is_reflection_token and e.created_at >= since
        )

    def _count_skill_cycle_reflections(
        self,
        skill_id: str,
        cycle_id: str
    ) -> int:
        """Count reflections for a skill in the current cycle"""
        # For now, just count recent skill reflections
        # In a full implementation, we'd track cycle_id in reflections
        entries = self.storage.get_journal_entries(limit=50)
        return sum(
            1 for e in entries
            if e.is_reflection_token and e.skill_id == skill_id
        )

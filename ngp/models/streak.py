"""Streak model - tracks consecutive completions"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional


@dataclass
class Streak:
    """
    Tracks consecutive day streaks for skills or overall.

    Attributes:
        id: Unique identifier
        skill_id: Optional skill being tracked (None = overall)
        current_streak: Current consecutive days
        longest_streak: Longest streak ever
        last_completion_date: Last date a completion was recorded
        created_at: When streak tracking started
    """
    id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_completion_date: Optional[date] = None
    skill_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def record_completion(self, completion_date: date) -> bool:
        """
        Record a completion. Returns True if streak increased.

        Args:
            completion_date: Date of completion

        Returns:
            True if streak was maintained/increased
        """
        if self.last_completion_date is None:
            # First completion
            self.current_streak = 1
            self.longest_streak = 1
            self.last_completion_date = completion_date
            return True

        # Check if this is the next day
        days_diff = (completion_date - self.last_completion_date).days

        if days_diff == 0:
            # Same day, no change to streak
            return True
        elif days_diff == 1:
            # Next day, increment streak
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
            self.last_completion_date = completion_date
            return True
        else:
            # Streak broken
            self.current_streak = 1
            self.last_completion_date = completion_date
            return False

    def is_active(self, today: date) -> bool:
        """Check if streak is still active (completed today or yesterday)"""
        if self.last_completion_date is None:
            return False

        days_since = (today - self.last_completion_date).days
        return days_since <= 1

    def days_until_broken(self, today: date) -> int:
        """Days remaining until streak breaks (0 = must complete today)"""
        if self.last_completion_date is None:
            return 0

        days_since = (today - self.last_completion_date).days

        if days_since == 0:
            return 1  # Completed today, safe until tomorrow
        elif days_since == 1:
            return 0  # Must complete today
        else:
            return -1  # Already broken

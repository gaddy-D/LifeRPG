"""Mission model - represents tasks/quests"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class ScheduleType(Enum):
    """Mission schedule types"""
    ONE_OFF = "one_off"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


@dataclass
class Mission:
    """
    Represents a mission (task) the player can complete.

    Attributes:
        id: Unique identifier
        title: Mission title
        note: Optional description/notes
        skill_ids: List of skill IDs this mission contributes to (1-2 skills)
        difficulty: Difficulty rating (1-5)
        energy: Energy requirement (1-5)
        schedule: How often this mission recurs
        due_at: Optional due date
        is_archived: Whether mission is archived
        created_at: When mission was created
        updated_at: When mission was last updated
    """
    id: str
    title: str
    skill_ids: List[str] = field(default_factory=list)
    difficulty: int = 1  # 1-5
    energy: int = 1  # 1-5
    schedule: ScheduleType = ScheduleType.ONE_OFF
    note: Optional[str] = None
    due_at: Optional[datetime] = None
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate difficulty and energy are in range"""
        if not 1 <= self.difficulty <= 5:
            raise ValueError("Difficulty must be 1-5")
        if not 1 <= self.energy <= 5:
            raise ValueError("Energy must be 1-5")
        if len(self.skill_ids) > 2:
            raise ValueError("Mission can be assigned to at most 2 skills")

    def base_player_xp(self) -> int:
        """Calculate base player XP: 4 × difficulty"""
        return 4 * self.difficulty

    def base_skill_xp(self) -> int:
        """Calculate base skill XP: 8 × difficulty"""
        return 8 * self.difficulty

    def coins_reward(self) -> int:
        """Calculate coin reward: 2 × difficulty"""
        return 2 * self.difficulty

    def cycle_player_xp(self) -> int:
        """Calculate cycle bonus player XP: 40 × difficulty"""
        return 40 * self.difficulty

    def cycle_skill_xp(self) -> int:
        """Calculate cycle bonus skill XP: 80 × difficulty"""
        return 80 * self.difficulty

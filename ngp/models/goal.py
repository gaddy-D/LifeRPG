"""Goal model - represents long-term objectives"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class GoalStatus(Enum):
    """Goal status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class GoalType(Enum):
    """Types of goals"""
    MISSION_COUNT = "mission_count"  # Complete N missions
    SKILL_LEVEL = "skill_level"  # Reach skill level N
    PLAYER_LEVEL = "player_level"  # Reach player level N
    COIN_TARGET = "coin_target"  # Accumulate N coins
    STREAK = "streak"  # Maintain N day streak
    CUSTOM = "custom"  # Manual tracking


@dataclass
class Goal:
    """
    Represents a long-term goal.

    Attributes:
        id: Unique identifier
        title: Goal title
        description: Goal description
        goal_type: Type of goal
        target_value: Target to reach
        current_value: Current progress
        status: Goal status
        skill_id: Optional linked skill
        created_at: When goal was created
        completed_at: When goal was completed
        deadline: Optional deadline
        milestones: List of milestone values
    """
    id: str
    title: str
    description: str
    goal_type: GoalType
    target_value: int
    current_value: int = 0
    status: GoalStatus = GoalStatus.ACTIVE
    skill_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    milestones: List[int] = field(default_factory=list)

    def progress_percentage(self) -> float:
        """Calculate progress as percentage"""
        if self.target_value == 0:
            return 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)

    def is_complete(self) -> bool:
        """Check if goal is complete"""
        return self.current_value >= self.target_value

    def update_progress(self, new_value: int) -> bool:
        """
        Update progress. Returns True if goal just completed.
        """
        was_complete = self.is_complete()
        self.current_value = new_value

        if self.is_complete() and not was_complete:
            self.status = GoalStatus.COMPLETED
            self.completed_at = datetime.now()
            return True

        return False

    def next_milestone(self) -> Optional[int]:
        """Get next milestone to reach"""
        for milestone in sorted(self.milestones):
            if self.current_value < milestone:
                return milestone
        return None

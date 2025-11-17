"""Skill model - represents player's skills"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class CycleType(Enum):
    """Cycle cadence for skills"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


@dataclass
class Skill:
    """
    Represents a skill the player is developing.

    Attributes:
        id: Unique identifier
        name: Skill name (e.g., "Writing", "Cardio")
        description: Optional description
        color: Color for UI display (hex code)
        icon_key: Icon identifier
        level: Skill level
        xp: Current skill XP
        is_archived: Whether skill is archived
        is_focus: Whether this is a Focus skill (slower leveling, deeper mastery)
        order: Display order
        cycle_type: How often cycles occur (daily/weekly/monthly/custom)
        cycle_start: When current cycle started
        cycle_end: When current cycle ends
        target_mission_id: The hidden mission target for this cycle
        has_hit_target_this_cycle: Whether target was completed this cycle
        missions_count: Number of missions assigned to this skill
    """
    id: str
    name: str
    level: int = 1
    xp: int = 0
    color: str = "#3B82F6"  # Default blue
    icon_key: str = "⚡"
    description: Optional[str] = None
    is_archived: bool = False
    is_focus: bool = False
    order: int = 0
    cycle_type: CycleType = CycleType.WEEKLY
    cycle_start: Optional[datetime] = None
    cycle_end: Optional[datetime] = None
    target_mission_id: Optional[str] = None
    has_hit_target_this_cycle: bool = False
    missions_count: int = 0

    def is_ready(self) -> bool:
        """Check if skill has >= 8 missions (readiness threshold)"""
        return self.missions_count >= 8

    def add_xp(self, amount: int) -> bool:
        """
        Add XP to skill. Returns True if leveled up.
        Accounts for Focus mode (2x XP requirement).
        """
        self.xp += amount
        xp_needed = self.xp_for_next_level()

        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            return True
        return False

    def xp_for_next_level(self) -> int:
        """
        Calculate XP needed for next level.
        Uses curve: ceil(120 × level^1.5)
        If Focus skill, multiply by 2 for slower progression.
        """
        import math
        base_xp = math.ceil(120 * (self.level ** 1.5))
        return base_xp * 2 if self.is_focus else base_xp

    def readiness_display(self) -> str:
        """Return readiness display string like '10/8' or '3/8'"""
        return f"{self.missions_count}/8"

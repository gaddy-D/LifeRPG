"""Completion model - records mission completions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Award:
    """XP and coin awards from a completion"""
    base_player_xp: int
    base_skill_xp_map: Dict[str, int]  # skill_id -> xp amount
    coins: int
    cycle_xp_applied_skill_id: Optional[str] = None  # If cycle bonus was applied


@dataclass
class Completion:
    """
    Records a mission completion event.

    Attributes:
        id: Unique identifier
        mission_id: ID of completed mission
        completed_at: When mission was completed
        award: XP and coins awarded
        cycle_id: Cycle identifier for one-credit-per-cycle tracking
        reflection_requested: Whether a reflection prompt was shown
    """
    id: str
    mission_id: str
    completed_at: datetime
    award: Award
    cycle_id: str  # Format: "skill_id:cycle_start_iso"
    reflection_requested: bool = False

    def __post_init__(self):
        if self.completed_at is None:
            self.completed_at = datetime.now()

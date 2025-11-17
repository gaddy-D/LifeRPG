"""Cycle service - manages skill cycles and targets"""

import random
from datetime import datetime, timedelta
from typing import List, Optional
from ..models import Skill, Mission
from ..models.skill import CycleType


class CycleService:
    """
    Manages per-skill cycles, target selection, and cycle boundaries.
    Implements the anti-Goodhart mechanics from the OuRPG spec.
    """

    @staticmethod
    def create_cycle_id(skill_id: str, cycle_start: datetime) -> str:
        """
        Create cycle ID for one-credit-per-cycle tracking.
        Format: "skill_id:cycle_start_iso"
        """
        return f"{skill_id}:{cycle_start.isoformat()}"

    @staticmethod
    def should_start_new_cycle(skill: Skill, current_time: datetime) -> bool:
        """
        Check if skill needs a new cycle started.

        Args:
            skill: Skill to check
            current_time: Current time

        Returns:
            True if cycle should be started
        """
        if skill.cycle_end is None:
            return True
        return current_time >= skill.cycle_end

    @staticmethod
    def calculate_cycle_boundaries(
        cycle_type: CycleType,
        current_time: datetime,
        day_starts_at: int = 0
    ) -> tuple[datetime, datetime]:
        """
        Calculate cycle start and end times based on cycle type.

        Args:
            cycle_type: Type of cycle (daily/weekly/monthly)
            current_time: Current time
            day_starts_at: Hour when day starts (0-23)

        Returns:
            Tuple of (cycle_start, cycle_end)
        """
        # Align to day start hour
        aligned_time = current_time.replace(hour=day_starts_at, minute=0, second=0, microsecond=0)

        if cycle_type == CycleType.DAILY:
            cycle_start = aligned_time
            cycle_end = cycle_start + timedelta(days=1)

        elif cycle_type == CycleType.WEEKLY:
            # Start of current week (Monday)
            days_since_monday = aligned_time.weekday()
            cycle_start = aligned_time - timedelta(days=days_since_monday)
            cycle_end = cycle_start + timedelta(weeks=1)

        elif cycle_type == CycleType.MONTHLY:
            # Start of current month
            cycle_start = aligned_time.replace(day=1)
            # Start of next month
            if cycle_start.month == 12:
                cycle_end = cycle_start.replace(year=cycle_start.year + 1, month=1)
            else:
                cycle_end = cycle_start.replace(month=cycle_start.month + 1)

        else:  # CUSTOM - treat as weekly for now
            days_since_monday = aligned_time.weekday()
            cycle_start = aligned_time - timedelta(days=days_since_monday)
            cycle_end = cycle_start + timedelta(weeks=1)

        return (cycle_start, cycle_end)

    @staticmethod
    def select_target_mission(missions: List[Mission]) -> Optional[str]:
        """
        Randomly select a target mission from the list.
        Uses uniform distribution.

        Args:
            missions: List of missions assigned to the skill

        Returns:
            Mission ID of selected target, or None if no missions
        """
        if not missions:
            return None
        return random.choice(missions).id

    @staticmethod
    def start_new_cycle(
        skill: Skill,
        missions: List[Mission],
        current_time: datetime,
        day_starts_at: int = 0
    ):
        """
        Start a new cycle for a skill.
        Sets cycle boundaries, selects target if ready.

        Args:
            skill: Skill to start cycle for
            missions: Missions assigned to this skill
            current_time: Current time
            day_starts_at: Hour when day starts
        """
        # Calculate cycle boundaries
        cycle_start, cycle_end = CycleService.calculate_cycle_boundaries(
            skill.cycle_type,
            current_time,
            day_starts_at
        )

        skill.cycle_start = cycle_start
        skill.cycle_end = cycle_end
        skill.has_hit_target_this_cycle = False

        # Only set target if skill is ready (>= 8 missions)
        skill.missions_count = len(missions)
        if skill.is_ready():
            skill.target_mission_id = CycleService.select_target_mission(missions)
        else:
            skill.target_mission_id = None

    @staticmethod
    def finalize_cycle(skill: Skill):
        """
        Finalize the current cycle.
        Currently a no-op, but could record cycle stats here.

        Args:
            skill: Skill to finalize cycle for
        """
        # Could track cycle completion stats here
        pass

    @staticmethod
    def is_target_hit(skill: Skill, mission_id: str) -> bool:
        """
        Check if completing this mission hits the cycle target.

        Args:
            skill: Skill to check
            mission_id: Mission being completed

        Returns:
            True if this is the target and it hasn't been hit yet
        """
        return (
            skill.target_mission_id == mission_id
            and not skill.has_hit_target_this_cycle
        )

    @staticmethod
    def mark_target_hit(skill: Skill):
        """Mark that the cycle target has been hit"""
        skill.has_hit_target_this_cycle = True

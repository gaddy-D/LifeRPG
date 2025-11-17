"""
Adjustment Loop - Player tweaks and refines their approach.

[Suggestion Loop]
      ↓
[Player Adjustment] → (User tweaks cadence, tasks, focus)
      ↓
Back to [Action Loop]
"""

from typing import List, Optional
from ..models import Skill, Mission, Player
from ..models.skill import CycleType
from ..services import StorageService, CycleService


class AdjustmentLoop:
    """
    Provides tools for players to adjust their approach:
    - Change cycle cadence (daily/weekly/monthly)
    - Toggle Focus mode on skills
    - Reorganize missions
    - Adjust difficulty/energy ratings
    """

    def __init__(self, storage: StorageService):
        self.storage = storage
        self.cycle_service = CycleService()

    def change_skill_cadence(
        self,
        skill_id: str,
        new_cadence: CycleType,
        day_starts_at: int = 0
    ) -> Skill:
        """
        Change the cycle cadence for a skill.

        Args:
            skill_id: Skill to modify
            new_cadence: New cycle type (daily/weekly/monthly)
            day_starts_at: When the day starts (for cycle calculations)

        Returns:
            Updated Skill object
        """
        skill = self.storage.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")

        # Update cycle type
        skill.cycle_type = new_cadence

        # Recalculate cycle boundaries
        from datetime import datetime
        missions = self._get_missions_for_skill(skill_id)
        self.cycle_service.start_new_cycle(
            skill,
            missions,
            datetime.now(),
            day_starts_at
        )

        self.storage.save_skill(skill)
        return skill

    def toggle_focus_mode(self, skill_id: str) -> Skill:
        """
        Toggle Focus mode for a skill.
        Focus mode = 2x XP requirement for leveling (deeper mastery).

        Args:
            skill_id: Skill to modify

        Returns:
            Updated Skill object
        """
        skill = self.storage.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")

        skill.is_focus = not skill.is_focus
        self.storage.save_skill(skill)
        return skill

    def adjust_mission_difficulty(self, mission_id: str, new_difficulty: int) -> Mission:
        """
        Adjust mission difficulty (1-5).

        Args:
            mission_id: Mission to modify
            new_difficulty: New difficulty rating (1-5)

        Returns:
            Updated Mission object
        """
        mission = self.storage.get_mission(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        if not 1 <= new_difficulty <= 5:
            raise ValueError("Difficulty must be 1-5")

        mission.difficulty = new_difficulty
        self.storage.save_mission(mission)
        return mission

    def adjust_mission_energy(self, mission_id: str, new_energy: int) -> Mission:
        """
        Adjust mission energy requirement (1-5).

        Args:
            mission_id: Mission to modify
            new_energy: New energy rating (1-5)

        Returns:
            Updated Mission object
        """
        mission = self.storage.get_mission(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        if not 1 <= new_energy <= 5:
            raise ValueError("Energy must be 1-5")

        mission.energy = new_energy
        self.storage.save_mission(mission)
        return mission

    def reassign_mission_skills(
        self,
        mission_id: str,
        new_skill_ids: List[str]
    ) -> Mission:
        """
        Reassign a mission to different skills (max 2).

        Args:
            mission_id: Mission to modify
            new_skill_ids: New skill IDs (1-2)

        Returns:
            Updated Mission object
        """
        mission = self.storage.get_mission(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        if len(new_skill_ids) > 2:
            raise ValueError("Mission can be assigned to at most 2 skills")

        # Update old skills' mission counts
        for old_skill_id in mission.skill_ids:
            skill = self.storage.get_skill(old_skill_id)
            if skill:
                missions = self._get_missions_for_skill(old_skill_id)
                skill.missions_count = len([m for m in missions if m.id != mission_id])
                self.storage.save_skill(skill)

        # Update mission
        mission.skill_ids = new_skill_ids

        # Update new skills' mission counts
        for new_skill_id in new_skill_ids:
            skill = self.storage.get_skill(new_skill_id)
            if skill:
                missions = self._get_missions_for_skill(new_skill_id)
                skill.missions_count = len(missions) + 1
                self.storage.save_skill(skill)

        self.storage.save_mission(mission)
        return mission

    def archive_skill(self, skill_id: str) -> Skill:
        """Archive a skill (hide from active view)"""
        skill = self.storage.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")

        skill.is_archived = True
        self.storage.save_skill(skill)
        return skill

    def archive_mission(self, mission_id: str) -> Mission:
        """Archive a mission (hide from active view)"""
        mission = self.storage.get_mission(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        mission.is_archived = True

        # Update skill mission counts
        for skill_id in mission.skill_ids:
            skill = self.storage.get_skill(skill_id)
            if skill:
                missions = self._get_missions_for_skill(skill_id)
                skill.missions_count = len([m for m in missions if not m.is_archived and m.id != mission_id])
                self.storage.save_skill(skill)

        self.storage.save_mission(mission)
        return mission

    def _get_missions_for_skill(self, skill_id: str) -> List[Mission]:
        """Get all active missions for a skill"""
        all_missions = self.storage.get_missions(include_archived=False)
        return [m for m in all_missions if skill_id in m.skill_ids]

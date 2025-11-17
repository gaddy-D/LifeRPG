"""
Action Loop - The primary gameplay loop where missions are completed.

[Action Loop] → (Missions, completions)
      ↓
[Reflection Loop]
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict
from ..models import Mission, Completion, Player, Skill
from ..models.completion import Award
from ..services import StorageService, ProgressionService, CycleService


class ActionLoop:
    """
    Manages the action loop: creating and completing missions.
    This is where the player takes action in the game.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage
        self.progression = ProgressionService()
        self.cycle = CycleService()

    def create_mission(
        self,
        title: str,
        skill_ids: List[str],
        difficulty: int = 1,
        energy: int = 1,
        note: Optional[str] = None
    ) -> Mission:
        """
        Create a new mission.

        Args:
            title: Mission title
            skill_ids: List of 1-2 skill IDs this mission contributes to
            difficulty: 1-5 difficulty rating
            energy: 1-5 energy requirement
            note: Optional notes

        Returns:
            Created Mission object
        """
        mission = Mission(
            id=str(uuid.uuid4()),
            title=title,
            skill_ids=skill_ids,
            difficulty=difficulty,
            energy=energy,
            note=note
        )

        self.storage.save_mission(mission)

        # Update missions_count for affected skills
        for skill_id in skill_ids:
            skill = self.storage.get_skill(skill_id)
            if skill:
                missions = self._get_missions_for_skill(skill_id)
                skill.missions_count = len(missions)
                self.storage.save_skill(skill)

        return mission

    def complete_mission(
        self,
        mission_id: str,
        player: Player
    ) -> Dict[str, any]:
        """
        Complete a mission and award XP/coins.
        Implements one-credit-per-cycle and cycle target mechanics.

        Args:
            mission_id: ID of mission to complete
            player: The player completing the mission

        Returns:
            Dict with completion details and rewards earned
        """
        mission = self.storage.get_mission(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        # Check cycles and update if needed
        self._update_all_cycles(player.day_starts_at)

        # Calculate base awards
        award = self.progression.calculate_base_awards(mission)

        # Track if cycle bonus applied
        cycle_bonus_applied_to: Optional[str] = None
        skill_level_ups = []
        player_leveled_up = False

        # Process each skill attached to this mission
        for skill_id in mission.skill_ids:
            skill = self.storage.get_skill(skill_id)
            if not skill:
                continue

            # Check if already credited this cycle
            cycle_id = self.cycle.create_cycle_id(skill_id, skill.cycle_start)
            existing_completions = self.storage.get_completions_for_mission_in_cycle(
                mission_id, cycle_id
            )

            if existing_completions:
                # Already credited this cycle - skip
                continue

            # Apply base skill XP
            skill_leveled_up = self.progression.apply_xp_to_skill(
                skill,
                award.base_skill_xp_map.get(skill_id, 0)
            )
            if skill_leveled_up:
                skill_level_ups.append(skill.name)

            # Check if this mission hits the cycle target
            if self.cycle.is_target_hit(skill, mission_id):
                # Apply cycle bonus
                player_cycle_xp, skill_cycle_xp = self.progression.calculate_cycle_bonus(
                    mission, skill
                )

                # Add to player
                player_leveled_up = self.progression.apply_xp_to_player(
                    player, player_cycle_xp
                ) or player_leveled_up

                # Add to skill
                skill_leveled_up = self.progression.apply_xp_to_skill(
                    skill, skill_cycle_xp
                ) or skill_leveled_up

                # Mark target as hit
                self.cycle.mark_target_hit(skill)
                cycle_bonus_applied_to = skill_id
                award.cycle_xp_applied_skill_id = skill_id

            self.storage.save_skill(skill)

        # Apply base player XP and coins
        player_leveled_up = self.progression.apply_xp_to_player(
            player, award.base_player_xp
        ) or player_leveled_up

        self.progression.apply_coins_to_player(player, award.coins)
        self.storage.save_player(player)

        # Create completion record
        skill = self.storage.get_skill(mission.skill_ids[0]) if mission.skill_ids else None
        cycle_id = self.cycle.create_cycle_id(
            mission.skill_ids[0],
            skill.cycle_start
        ) if skill else "no_skill"

        completion = Completion(
            id=str(uuid.uuid4()),
            mission_id=mission_id,
            completed_at=datetime.now(),
            award=award,
            cycle_id=cycle_id
        )

        self.storage.save_completion(completion)

        return {
            'completion': completion,
            'player_leveled_up': player_leveled_up,
            'skill_level_ups': skill_level_ups,
            'cycle_bonus_applied': cycle_bonus_applied_to is not None,
            'xp_earned': award.base_player_xp,
            'coins_earned': award.coins
        }

    def _get_missions_for_skill(self, skill_id: str) -> List[Mission]:
        """Get all active missions for a skill"""
        all_missions = self.storage.get_missions(include_archived=False)
        return [m for m in all_missions if skill_id in m.skill_ids]

    def _update_all_cycles(self, day_starts_at: int):
        """Check and update cycles for all skills"""
        skills = self.storage.get_skills(include_archived=False)
        current_time = datetime.now()

        for skill in skills:
            if self.cycle.should_start_new_cycle(skill, current_time):
                # Finalize old cycle
                self.cycle.finalize_cycle(skill)

                # Start new cycle
                missions = self._get_missions_for_skill(skill.id)
                self.cycle.start_new_cycle(skill, missions, current_time, day_starts_at)
                self.storage.save_skill(skill)

    def get_available_missions(
        self,
        player: Player,
        energy_filter: Optional[int] = None
    ) -> List[Mission]:
        """
        Get available missions, optionally filtered by energy level.

        Args:
            player: Current player
            energy_filter: Optional energy level to filter by

        Returns:
            List of available missions
        """
        missions = self.storage.get_missions(include_archived=False)

        if energy_filter:
            missions = [m for m in missions if m.energy == energy_filter]

        return missions

"""Progression service - handles XP, leveling, and rewards"""

from typing import Dict, Optional, Tuple
from ..models import Player, Skill, Mission
from ..models.completion import Award


class ProgressionService:
    """
    Handles all XP calculations, leveling logic, and reward distribution.
    Implements the core mechanics from the OuRPG spec.
    """

    @staticmethod
    def calculate_base_awards(mission: Mission) -> Award:
        """
        Calculate base XP and coins for completing a mission.
        Does NOT include cycle bonuses.

        Returns:
            Award with base player XP, base skill XP map, and coins
        """
        base_player_xp = mission.base_player_xp()  # 4 × difficulty
        coins = mission.coins_reward()  # 2 × difficulty

        # Base skill XP: 8 × difficulty per attached skill
        base_skill_xp_map = {}
        for skill_id in mission.skill_ids:
            base_skill_xp_map[skill_id] = mission.base_skill_xp()

        return Award(
            base_player_xp=base_player_xp,
            base_skill_xp_map=base_skill_xp_map,
            coins=coins
        )

    @staticmethod
    def calculate_cycle_bonus(mission: Mission, skill: Skill) -> Tuple[int, int]:
        """
        Calculate cycle bonus XP when target mission is hit.

        Args:
            mission: The mission being completed
            skill: The skill that had this mission as its target

        Returns:
            Tuple of (player_cycle_xp, skill_cycle_xp)
        """
        player_cycle_xp = mission.cycle_player_xp()  # 40 × difficulty
        skill_cycle_xp = mission.cycle_skill_xp()  # 80 × difficulty
        return (player_cycle_xp, skill_cycle_xp)

    @staticmethod
    def apply_xp_to_player(player: Player, xp: int) -> bool:
        """
        Apply XP to player and handle level-ups.

        Args:
            player: Player to apply XP to
            xp: Amount of XP to add

        Returns:
            True if player leveled up, False otherwise
        """
        return player.add_xp(xp)

    @staticmethod
    def apply_xp_to_skill(skill: Skill, xp: int) -> bool:
        """
        Apply XP to skill and handle level-ups.
        Accounts for Focus mode (2x XP requirement).

        Args:
            skill: Skill to apply XP to
            xp: Amount of XP to add

        Returns:
            True if skill leveled up, False otherwise
        """
        return skill.add_xp(xp)

    @staticmethod
    def apply_coins_to_player(player: Player, coins: int):
        """Add coins to player"""
        player.add_coins(coins)

    @staticmethod
    def get_player_progress_display(player: Player) -> Dict[str, any]:
        """
        Get player progress information for UI display.

        Returns:
            Dict with level, current XP, XP needed, percentage, coins
        """
        xp_needed = player.xp_for_next_level()
        percentage = (player.xp / xp_needed) * 100 if xp_needed > 0 else 0

        return {
            'level': player.level,
            'xp': player.xp,
            'xp_needed': xp_needed,
            'percentage': percentage,
            'coins': player.coins
        }

    @staticmethod
    def get_skill_progress_display(skill: Skill) -> Dict[str, any]:
        """
        Get skill progress information for UI display.

        Returns:
            Dict with level, current XP, XP needed, percentage, is_focus, is_ready
        """
        xp_needed = skill.xp_for_next_level()
        percentage = (skill.xp / xp_needed) * 100 if xp_needed > 0 else 0

        return {
            'level': skill.level,
            'xp': skill.xp,
            'xp_needed': xp_needed,
            'percentage': percentage,
            'is_focus': skill.is_focus,
            'is_ready': skill.is_ready(),
            'readiness': skill.readiness_display()
        }

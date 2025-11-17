"""Streaks service - track consecutive completions"""

import uuid
from typing import Optional, List, Dict
from datetime import date, datetime
from ..models import Streak
from ..services import StorageService


class StreaksService:
    """
    Manages streak tracking for skills and overall progress.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def get_or_create_streak(self, skill_id: Optional[str] = None) -> Streak:
        """
        Get existing streak or create new one.

        Args:
            skill_id: Skill ID (None for overall streak)

        Returns:
            Streak object
        """
        streak = self.storage.get_streak_by_skill(skill_id)

        if not streak:
            streak = Streak(
                id=str(uuid.uuid4()),
                skill_id=skill_id
            )
            self.storage.save_streak(streak)

        return streak

    def record_completion(
        self,
        skill_id: Optional[str] = None,
        completion_date: Optional[date] = None
    ) -> Dict[str, any]:
        """
        Record a completion for streak tracking.

        Args:
            skill_id: Skill ID (None for overall)
            completion_date: Date of completion (default: today)

        Returns:
            Dict with streak info and status
        """
        if completion_date is None:
            completion_date = date.today()

        streak = self.get_or_create_streak(skill_id)
        old_streak = streak.current_streak

        streak_maintained = streak.record_completion(completion_date)
        self.storage.save_streak(streak)

        # Also update overall streak if this is a skill-specific completion
        if skill_id is not None:
            overall_streak = self.get_or_create_streak(None)
            overall_streak.record_completion(completion_date)
            self.storage.save_streak(overall_streak)

        return {
            'streak': streak,
            'streak_maintained': streak_maintained,
            'streak_increased': streak.current_streak > old_streak,
            'new_record': streak.current_streak == streak.longest_streak and streak.current_streak > 1
        }

    def get_all_streaks(self) -> Dict[str, Streak]:
        """
        Get all streaks.

        Returns:
            Dict with 'overall' and 'skills' keys
        """
        all_streaks = self.storage.get_streaks()

        overall = None
        skills = {}

        for streak in all_streaks:
            if streak.skill_id is None:
                overall = streak
            else:
                skills[streak.skill_id] = streak

        return {
            'overall': overall,
            'skills': skills
        }

    def get_streak_status(self, today: Optional[date] = None) -> Dict[str, any]:
        """
        Get status of all streaks.

        Args:
            today: Reference date (default: today)

        Returns:
            Dict with streak statuses
        """
        if today is None:
            today = date.today()

        streaks_data = self.get_all_streaks()
        overall = streaks_data['overall']

        status = {
            'overall_active': overall.is_active(today) if overall else False,
            'overall_current': overall.current_streak if overall else 0,
            'overall_longest': overall.longest_streak if overall else 0,
            'skills_active': 0,
            'skills_at_risk': 0,  # Must complete today
            'total_skills': len(streaks_data['skills'])
        }

        for skill_id, streak in streaks_data['skills'].items():
            if streak.is_active(today):
                status['skills_active'] += 1

            days_left = streak.days_until_broken(today)
            if days_left == 0:
                status['skills_at_risk'] += 1

        return status

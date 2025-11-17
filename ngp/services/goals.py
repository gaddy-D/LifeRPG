"""Goals service - manage long-term objectives"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime
from ..models import Goal, GoalType, GoalStatus, Player, Skill
from ..services import StorageService


class GoalsService:
    """
    Manages goals and tracks progress toward objectives.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def create_goal(
        self,
        title: str,
        description: str,
        goal_type: GoalType,
        target_value: int,
        skill_id: Optional[str] = None,
        deadline: Optional[datetime] = None,
        milestones: Optional[List[int]] = None
    ) -> Goal:
        """
        Create a new goal.

        Args:
            title: Goal title
            description: Goal description
            goal_type: Type of goal
            target_value: Target to reach
            skill_id: Optional linked skill
            deadline: Optional deadline
            milestones: Optional milestone values

        Returns:
            Created Goal
        """
        goal = Goal(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            goal_type=goal_type,
            target_value=target_value,
            skill_id=skill_id,
            deadline=deadline,
            milestones=milestones or []
        )

        self.storage.save_goal(goal)
        return goal

    def update_goal_progress(self, goal_id: str, new_value: int) -> Dict[str, any]:
        """
        Update goal progress.

        Args:
            goal_id: ID of goal to update
            new_value: New progress value

        Returns:
            Dict with update info
        """
        goal = self.storage.get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")

        old_value = goal.current_value
        just_completed = goal.update_progress(new_value)

        # Check for milestone achievements
        milestone_hit = None
        next_milestone = goal.next_milestone()
        if next_milestone and old_value < next_milestone <= new_value:
            milestone_hit = next_milestone

        self.storage.save_goal(goal)

        return {
            'goal': goal,
            'just_completed': just_completed,
            'milestone_hit': milestone_hit,
            'progress_percentage': goal.progress_percentage()
        }

    def check_and_update_goals(
        self,
        player: Player,
        skills: List[Skill],
        mission_count: Optional[Dict[str, int]] = None
    ) -> List[Dict]:
        """
        Check all active goals and update progress.

        Args:
            player: Current player
            skills: Current skills
            mission_count: Optional mission count per skill

        Returns:
            List of goals that were updated
        """
        active_goals = self.storage.get_goals(status='active')
        updated = []

        for goal in active_goals:
            new_value = None

            if goal.goal_type == GoalType.PLAYER_LEVEL:
                new_value = player.level

            elif goal.goal_type == GoalType.COIN_TARGET:
                new_value = player.coins

            elif goal.goal_type == GoalType.SKILL_LEVEL and goal.skill_id:
                skill = next((s for s in skills if s.id == goal.skill_id), None)
                if skill:
                    new_value = skill.level

            elif goal.goal_type == GoalType.MISSION_COUNT and mission_count:
                if goal.skill_id:
                    new_value = mission_count.get(goal.skill_id, 0)
                else:
                    new_value = sum(mission_count.values())

            if new_value is not None and new_value != goal.current_value:
                result = self.update_goal_progress(goal.id, new_value)
                updated.append(result)

        return updated

    def get_active_goals(self) -> List[Goal]:
        """Get all active goals"""
        return self.storage.get_goals(status='active')

    def get_completed_goals(self) -> List[Goal]:
        """Get all completed goals"""
        return self.storage.get_goals(status='completed')

    def archive_goal(self, goal_id: str):
        """Archive a goal"""
        goal = self.storage.get_goal(goal_id)
        if goal:
            goal.status = GoalStatus.ARCHIVED
            self.storage.save_goal(goal)

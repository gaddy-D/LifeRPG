"""Metrics service - calculates Variety and Consistency scores"""

from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import math
from ..models import Skill, Mission, Completion
from ..services import StorageService


class MetricsService:
    """
    Calculates Variety and Consistency scores for skills.

    - Variety: How evenly missions are distributed in current cycle
    - Consistency: Rolling success rate for hitting cycle targets
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def calculate_variety(self, skill: Skill) -> Optional[Dict[str, any]]:
        """
        Calculate variety score for a skill in the current cycle.
        Uses entropy-based calculation to measure evenness of distribution.

        Args:
            skill: Skill to calculate variety for

        Returns:
            Dict with score (0.0-1.0), rating (low/fair/good), and details
        """
        if not skill.cycle_start:
            return None

        # Get all missions for this skill
        all_missions = self.storage.get_missions(include_archived=False)
        skill_missions = [m for m in all_missions if skill.id in m.skill_ids]

        if len(skill_missions) < 2:
            return None  # Need at least 2 missions to measure variety

        # Get completions in current cycle
        cycle_id = f"{skill.id}:{skill.cycle_start.isoformat()}"

        # Count completions per mission
        mission_counts = defaultdict(int)
        total_completions = 0

        # This is simplified - in production we'd query completions by cycle_id
        # For now, we'll use a heuristic
        for mission in skill_missions:
            # Check if mission was completed in this cycle
            completions = self.storage.get_completions_for_mission_in_cycle(
                mission.id, cycle_id
            )
            count = len(completions)
            if count > 0:
                mission_counts[mission.id] = count
                total_completions += count

        if total_completions == 0:
            return {
                'score': 0.0,
                'rating': 'none',
                'message': 'No completions in current cycle'
            }

        # Calculate entropy (higher = more even distribution)
        entropy = 0.0
        for count in mission_counts.values():
            if count > 0:
                p = count / total_completions
                entropy -= p * math.log2(p)

        # Normalize to 0-1 (max entropy for N missions is log2(N))
        max_entropy = math.log2(len(skill_missions))
        variety_score = entropy / max_entropy if max_entropy > 0 else 0.0

        # Categorize
        if variety_score >= 0.7:
            rating = 'good'
        elif variety_score >= 0.4:
            rating = 'fair'
        else:
            rating = 'low'

        return {
            'score': variety_score,
            'rating': rating,
            'message': f'{len(mission_counts)} of {len(skill_missions)} missions completed',
            'total_completions': total_completions
        }

    def calculate_consistency(
        self,
        skill: Skill,
        lookback_cycles: int = 6
    ) -> Optional[Dict[str, any]]:
        """
        Calculate consistency score - rolling success rate for hitting cycle targets.

        Args:
            skill: Skill to calculate consistency for
            lookback_cycles: Number of cycles to look back

        Returns:
            Dict with score (0.0-1.0), rating, and details
        """
        if not skill.cycle_start:
            return None

        # For v1.1, we'll use a simple metric: has target been hit this cycle?
        # In a full implementation, we'd track historical cycle completions

        # Current cycle status
        current_hit = skill.has_hit_target_this_cycle

        # Simple consistency: binary for now
        # TODO: Track historical cycle performance in database
        if current_hit:
            score = 1.0
            rating = 'excellent'
            message = 'Target hit this cycle'
        else:
            score = 0.0
            rating = 'needs work'
            message = 'Target not yet hit'

        return {
            'score': score,
            'rating': rating,
            'message': message
        }

    def get_skill_metrics(self, skill: Skill) -> Dict[str, Optional[Dict]]:
        """
        Get all metrics for a skill.

        Returns:
            Dict with 'variety' and 'consistency' keys
        """
        return {
            'variety': self.calculate_variety(skill),
            'consistency': self.calculate_consistency(skill)
        }

    def get_variety_chip(self, skill: Skill) -> str:
        """
        Get variety chip text for UI display.

        Returns:
            String like "Variety: good" or ""
        """
        variety = self.calculate_variety(skill)
        if not variety:
            return ""

        rating = variety['rating']
        if rating == 'none':
            return ""

        colors = {
            'good': 'green',
            'fair': 'yellow',
            'low': 'red',
        }
        color = colors.get(rating, 'white')

        return f"[{color}]Variety: {rating}[/{color}]"

    def get_consistency_chip(self, skill: Skill) -> str:
        """
        Get consistency chip text for UI display.

        Returns:
            String like "Consistency: excellent" or ""
        """
        consistency = self.calculate_consistency(skill)
        if not consistency:
            return ""

        rating = consistency['rating']

        colors = {
            'excellent': 'green',
            'good': 'cyan',
            'needs work': 'yellow',
            'poor': 'red',
        }
        color = colors.get(rating, 'white')

        return f"[{color}]Consistency: {rating}[/{color}]"

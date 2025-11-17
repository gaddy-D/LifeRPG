"""
Analysis Loop - The Navigator interprets patterns and insights.

[Reflection Loop]
      ↓
[Analysis Loop] → (Navigator interprets patterns)
      ↓
[Suggestion Loop]
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from ..models import Skill, Mission, Completion, JournalEntry
from ..services import StorageService


class Pattern:
    """Represents a detected pattern"""
    def __init__(self, type: str, description: str, confidence: float, data: Dict):
        self.type = type
        self.description = description
        self.confidence = confidence  # 0.0 to 1.0
        self.data = data


class AnalysisLoop:
    """
    The Navigator - analyzes player patterns and generates insights.
    This is the intelligence layer that detects trends and behaviors.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def analyze_player_patterns(self, lookback_days: int = 30) -> List[Pattern]:
        """
        Analyze player patterns over the lookback period.

        Args:
            lookback_days: How many days to look back

        Returns:
            List of detected patterns
        """
        patterns = []

        # Get data for analysis
        skills = self.storage.get_skills(include_archived=False)

        # Pattern 1: Skill focus imbalance
        focus_pattern = self._detect_skill_imbalance(skills)
        if focus_pattern:
            patterns.append(focus_pattern)

        # Pattern 2: Cycle target hit rate
        target_pattern = self._detect_cycle_performance(skills)
        if target_pattern:
            patterns.append(target_pattern)

        # Pattern 3: Skill readiness gaps
        readiness_pattern = self._detect_readiness_gaps(skills)
        if readiness_pattern:
            patterns.append(readiness_pattern)

        # Pattern 4: Reflection frequency
        reflection_pattern = self._detect_reflection_patterns()
        if reflection_pattern:
            patterns.append(reflection_pattern)

        return patterns

    def _detect_skill_imbalance(self, skills: List[Skill]) -> Optional[Pattern]:
        """Detect if player is focusing on one skill over others"""
        if len(skills) < 2:
            return None

        # Compare skill levels
        levels = [s.level for s in skills]
        avg_level = sum(levels) / len(levels)
        max_level = max(levels)
        min_level = min(levels)

        # If one skill is 3+ levels ahead, that's an imbalance
        if max_level - min_level >= 3:
            leading_skill = next(s for s in skills if s.level == max_level)
            return Pattern(
                type="skill_imbalance",
                description=f"Your {leading_skill.name} skill is {max_level - min_level} levels ahead of others",
                confidence=min(1.0, (max_level - min_level) / 5.0),
                data={'leading_skill': leading_skill.name, 'gap': max_level - min_level}
            )

        return None

    def _detect_cycle_performance(self, skills: List[Skill]) -> Optional[Pattern]:
        """Detect cycle target hit patterns"""
        ready_skills = [s for s in skills if s.is_ready()]
        if not ready_skills:
            return None

        hit_count = sum(1 for s in ready_skills if s.has_hit_target_this_cycle)
        total = len(ready_skills)
        hit_rate = hit_count / total if total > 0 else 0

        if hit_rate == 1.0:
            return Pattern(
                type="perfect_cycle",
                description=f"Perfect cycle! You've hit targets for all {total} ready skills",
                confidence=1.0,
                data={'hit_count': hit_count, 'total': total}
            )
        elif hit_rate < 0.3:
            return Pattern(
                type="low_cycle_performance",
                description=f"Only {hit_count}/{total} skills hit their cycle targets",
                confidence=0.7,
                data={'hit_count': hit_count, 'total': total}
            )

        return None

    def _detect_readiness_gaps(self, skills: List[Skill]) -> Optional[Pattern]:
        """Detect skills that need more missions"""
        not_ready = [s for s in skills if not s.is_ready() and not s.is_archived]
        if not not_ready:
            return None

        # Find the skill furthest from readiness
        furthest = min(not_ready, key=lambda s: s.missions_count)
        gap = 8 - furthest.missions_count

        return Pattern(
            type="readiness_gap",
            description=f"{furthest.name} needs {gap} more missions to be cycle-ready",
            confidence=0.8,
            data={'skill': furthest.name, 'current': furthest.missions_count, 'needed': 8}
        )

    def _detect_reflection_patterns(self) -> Optional[Pattern]:
        """Analyze reflection frequency"""
        entries = self.storage.get_journal_entries(limit=50)
        reflections = [e for e in entries if e.is_reflection_token]

        if len(reflections) == 0:
            return Pattern(
                type="no_reflections",
                description="You haven't written any reflections yet",
                confidence=1.0,
                data={'count': 0}
            )

        # Check time since last reflection
        last_reflection = reflections[0] if reflections else None
        if last_reflection:
            days_since = (datetime.now() - last_reflection.created_at).days
            if days_since > 7:
                return Pattern(
                    type="reflection_lapse",
                    description=f"It's been {days_since} days since your last reflection",
                    confidence=0.6,
                    data={'days_since': days_since}
                )

        return None

    def get_skill_variety_score(self, skill: Skill) -> Optional[float]:
        """
        Calculate variety score for a skill (how evenly missions are distributed).
        Returns 0.0 (low variety) to 1.0 (high variety).
        """
        # This would require tracking completions per mission within the cycle
        # For now, return None to indicate we need more data
        return None

    def get_skill_consistency_score(self, skill: Skill) -> Optional[float]:
        """
        Calculate consistency score (how often cycle targets are hit).
        Returns 0.0 (inconsistent) to 1.0 (very consistent).
        """
        # This would require tracking historical cycle performance
        # For now, return current cycle hit status as binary
        if not skill.is_ready():
            return None
        return 1.0 if skill.has_hit_target_this_cycle else 0.0

    def generate_insights(self) -> List[str]:
        """
        Generate human-readable insights from patterns.

        Returns:
            List of insight strings
        """
        patterns = self.analyze_player_patterns()
        insights = []

        for pattern in patterns:
            if pattern.confidence >= 0.6:
                insights.append(pattern.description)

        return insights

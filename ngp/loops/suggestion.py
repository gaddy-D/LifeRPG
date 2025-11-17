"""
Suggestion Loop - Provides subtle corrective feedback based on analysis.

[Analysis Loop]
      ↓
[Suggestion Loop] → (Subtle corrective feedback)
      ↓
[Player Adjustment]
"""

from typing import List, Optional
from .analysis import AnalysisLoop, Pattern
from ..models import Player, Skill
from ..services import StorageService


class Suggestion:
    """Represents a suggestion to the player"""
    def __init__(
        self,
        title: str,
        message: str,
        action_hint: Optional[str] = None,
        priority: str = "normal"  # low, normal, high
    ):
        self.title = title
        self.message = message
        self.action_hint = action_hint
        self.priority = priority


class SuggestionLoop:
    """
    Generates subtle, non-intrusive suggestions based on Navigator analysis.
    Provides corrective feedback without being pushy or manipulative.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage
        self.analysis = AnalysisLoop(storage)

    def generate_suggestions(self, max_suggestions: int = 3) -> List[Suggestion]:
        """
        Generate contextual suggestions for the player.

        Args:
            max_suggestions: Maximum number of suggestions to return

        Returns:
            List of Suggestion objects, ordered by priority
        """
        suggestions = []

        # Analyze current state
        patterns = self.analysis.analyze_player_patterns()

        # Convert patterns to suggestions
        for pattern in patterns:
            suggestion = self._pattern_to_suggestion(pattern)
            if suggestion:
                suggestions.append(suggestion)

        # Check for basic setup needs
        setup_suggestions = self._check_setup_needs()
        suggestions.extend(setup_suggestions)

        # Sort by priority and limit
        priority_order = {"high": 0, "normal": 1, "low": 2}
        suggestions.sort(key=lambda s: priority_order[s.priority])

        return suggestions[:max_suggestions]

    def _pattern_to_suggestion(self, pattern: Pattern) -> Optional[Suggestion]:
        """Convert a detected pattern into an actionable suggestion"""

        if pattern.type == "skill_imbalance":
            return Suggestion(
                title="Skill Balance",
                message=pattern.description,
                action_hint="Consider creating missions for your other skills",
                priority="normal"
            )

        elif pattern.type == "perfect_cycle":
            return Suggestion(
                title="Perfect Cycle!",
                message=pattern.description,
                action_hint="Keep up the balanced approach",
                priority="low"
            )

        elif pattern.type == "low_cycle_performance":
            return Suggestion(
                title="Cycle Targets",
                message=pattern.description,
                action_hint="Try to complete a variety of missions for each skill",
                priority="normal"
            )

        elif pattern.type == "readiness_gap":
            skill_name = pattern.data.get('skill', '')
            gap = pattern.data.get('needed', 8) - pattern.data.get('current', 0)
            return Suggestion(
                title=f"{skill_name} Needs Missions",
                message=f"Add {gap} more missions to unlock cycle bonuses",
                action_hint="Each skill needs 8+ missions to be cycle-ready",
                priority="high"
            )

        elif pattern.type == "no_reflections":
            return Suggestion(
                title="Reflection",
                message="Try writing a reflection after completing missions",
                action_hint="Reflections help track your growth journey",
                priority="low"
            )

        elif pattern.type == "reflection_lapse":
            days = pattern.data.get('days_since', 0)
            return Suggestion(
                title="Time to Reflect",
                message=f"It's been {days} days since your last reflection",
                action_hint="Open the journal to write a new entry",
                priority="normal"
            )

        return None

    def _check_setup_needs(self) -> List[Suggestion]:
        """Check if player needs basic setup guidance"""
        suggestions = []

        skills = self.storage.get_skills(include_archived=False)
        missions = self.storage.get_missions(include_archived=False)

        # No skills created yet
        if len(skills) == 0:
            suggestions.append(Suggestion(
                title="Get Started",
                message="Create your first skill to begin your journey",
                action_hint="Skills represent areas you want to develop (e.g., Writing, Fitness)",
                priority="high"
            ))

        # Skills but no missions
        elif len(missions) == 0:
            suggestions.append(Suggestion(
                title="Create Missions",
                message="Create missions to start earning XP",
                action_hint="Missions are tasks that help you develop your skills",
                priority="high"
            ))

        # Has skills and missions, check if any skill is ready
        elif len(skills) > 0:
            ready_count = sum(1 for s in skills if s.is_ready())
            if ready_count == 0:
                suggestions.append(Suggestion(
                    title="Reach Readiness",
                    message="Get your skills to 8+ missions to unlock cycle bonuses",
                    action_hint="Cycle bonuses provide 10x more XP",
                    priority="normal"
                ))

        return suggestions

    def get_next_action_hint(self) -> str:
        """
        Get a single, concise hint for what to do next.

        Returns:
            A short string suggesting the next action
        """
        suggestions = self.generate_suggestions(max_suggestions=1)

        if suggestions:
            return suggestions[0].message

        # Default hint
        return "Complete a mission to earn XP and progress your skills"

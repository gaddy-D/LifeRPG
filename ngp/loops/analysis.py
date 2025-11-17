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

        # Pattern 5: Focus skill analysis (v1.1)
        focus_analysis = self._analyze_focus_skills(skills)
        if focus_analysis:
            patterns.append(focus_analysis)

        # Pattern 6: Coin accumulation (v1.1)
        coin_pattern = self._detect_coin_patterns()
        if coin_pattern:
            patterns.append(coin_pattern)

        # Pattern 7: Mission difficulty distribution (v1.1)
        difficulty_pattern = self._analyze_mission_difficulty()
        if difficulty_pattern:
            patterns.append(difficulty_pattern)

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

    def _analyze_focus_skills(self, skills: List[Skill]) -> Optional[Pattern]:
        """Analyze focus skill usage (v1.1)"""
        focus_skills = [s for s in skills if s.is_focus]

        if not focus_skills:
            # Suggest using focus mode
            if len(skills) >= 2:
                return Pattern(
                    type="no_focus_skills",
                    description="Consider marking a skill as Focus for deeper mastery",
                    confidence=0.5,
                    data={'suggestion': 'focus_mode'}
                )
        elif len(focus_skills) > 2:
            # Too many focus skills
            return Pattern(
                type="too_many_focus",
                description=f"You have {len(focus_skills)} Focus skills - consider narrowing your focus",
                confidence=0.7,
                data={'count': len(focus_skills)}
            )

        return None

    def _detect_coin_patterns(self) -> Optional[Pattern]:
        """Analyze coin accumulation and spending (v1.1)"""
        player = self.storage.get_player()
        if not player:
            return None

        rewards = self.storage.get_rewards(include_archived=False)
        redemptions = self.storage.get_redemptions(limit=100)

        # High coins, no rewards defined
        if player.coins > 50 and len(rewards) == 0:
            return Pattern(
                type="no_rewards",
                description=f"You have {player.coins} coins! Create rewards to spend them on",
                confidence=0.8,
                data={'coins': player.coins}
            )

        # High coins, rewards exist but never redeemed
        if player.coins > 100 and len(rewards) > 0 and len(redemptions) == 0:
            return Pattern(
                type="coins_hoarding",
                description=f"You've accumulated {player.coins} coins - treat yourself to a reward!",
                confidence=0.7,
                data={'coins': player.coins, 'rewards_available': len(rewards)}
            )

        return None

    def _analyze_mission_difficulty(self) -> Optional[Pattern]:
        """Analyze mission difficulty distribution (v1.1)"""
        missions = self.storage.get_missions(include_archived=False)

        if not missions:
            return None

        difficulties = [m.difficulty for m in missions]
        avg_difficulty = sum(difficulties) / len(difficulties)

        # All missions are difficulty 1
        if all(d == 1 for d in difficulties) and len(missions) >= 5:
            return Pattern(
                type="all_easy_missions",
                description="All your missions are difficulty 1 - consider adding some challenges",
                confidence=0.7,
                data={'avg_difficulty': avg_difficulty}
            )

        # Very high average difficulty
        if avg_difficulty >= 4.5:
            return Pattern(
                type="very_hard_missions",
                description=f"Your missions average difficulty {avg_difficulty:.1f} - don't burn out!",
                confidence=0.6,
                data={'avg_difficulty': avg_difficulty}
            )

        return None

    def get_comprehensive_report(self) -> Dict[str, any]:
        """
        Generate a comprehensive analysis report (v1.1).

        Returns:
            Dict with all analysis data
        """
        player = self.storage.get_player()
        skills = self.storage.get_skills(include_archived=False)
        missions = self.storage.get_missions(include_archived=False)
        patterns = self.analyze_player_patterns()

        # Calculate statistics
        stats = {
            'player_level': player.level if player else 0,
            'total_coins': player.coins if player else 0,
            'active_skills': len(skills),
            'ready_skills': sum(1 for s in skills if s.is_ready()),
            'focus_skills': sum(1 for s in skills if s.is_focus),
            'total_missions': len(missions),
            'avg_mission_difficulty': sum(m.difficulty for m in missions) / len(missions) if missions else 0,
            'patterns_detected': len(patterns),
            'high_confidence_patterns': sum(1 for p in patterns if p.confidence >= 0.7)
        }

        # Extract key insights
        insights = self.generate_insights()

        return {
            'statistics': stats,
            'patterns': [
                {
                    'type': p.type,
                    'description': p.description,
                    'confidence': p.confidence,
                    'data': p.data
                }
                for p in patterns
            ],
            'insights': insights,
            'recommendations': self._generate_recommendations(patterns)
        }

    def _generate_recommendations(self, patterns: List[Pattern]) -> List[str]:
        """Generate actionable recommendations from patterns"""
        recommendations = []

        for pattern in patterns:
            if pattern.type == "readiness_gap":
                recommendations.append(
                    f"Add {pattern.data.get('needed', 8) - pattern.data.get('current', 0)} "
                    f"missions to {pattern.data.get('skill')} to unlock cycle bonuses"
                )

            elif pattern.type == "skill_imbalance":
                recommendations.append(
                    "Balance your effort across all skills for well-rounded growth"
                )

            elif pattern.type == "no_rewards":
                recommendations.append(
                    "Create rewards to give yourself something to work toward"
                )

            elif pattern.type == "all_easy_missions":
                recommendations.append(
                    "Add some difficulty 2-3 missions to earn more XP and coins"
                )

        return recommendations

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

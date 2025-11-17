"""Advanced statistics service - comprehensive data analysis and visualization"""

from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta, date
from ..models import Player, Skill, Mission, Completion
from ..services import StorageService


class StatisticsService:
    """
    Advanced statistics and data analysis.
    Provides comprehensive insights into player progress.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def get_comprehensive_stats(self) -> Dict[str, any]:
        """
        Generate comprehensive statistics across all game data.

        Returns:
            Dict with extensive statistics
        """
        player = self.storage.get_player()
        skills = self.storage.get_skills(include_archived=False)
        missions = self.storage.get_missions(include_archived=False)
        journal_entries = self.storage.get_journal_entries(limit=1000)
        goals = self.storage.get_goals()
        streaks = self.storage.get_streaks()
        rewards = self.storage.get_rewards()
        redemptions = self.storage.get_redemptions(limit=1000)

        stats = {
            'player': self._get_player_stats(player),
            'skills': self._get_skills_stats(skills),
            'missions': self._get_missions_stats(missions),
            'journal': self._get_journal_stats(journal_entries),
            'goals': self._get_goals_stats(goals),
            'streaks': self._get_streaks_stats(streaks),
            'economy': self._get_economy_stats(player, rewards, redemptions),
            'timeline': self._get_timeline_stats(),
            'trends': self._get_trends_stats(),
        }

        return stats

    def _get_player_stats(self, player: Optional[Player]) -> Dict:
        """Player statistics"""
        if not player:
            return {}

        days_since_start = (datetime.now() - player.created_at).days
        xp_per_day = player.xp / days_since_start if days_since_start > 0 else 0

        return {
            'level': player.level,
            'total_xp': player.xp,
            'coins': player.coins,
            'class': player.class_name,
            'days_playing': days_since_start,
            'xp_per_day': round(xp_per_day, 1),
            'xp_for_next_level': player.xp_for_next_level(),
            'progress_to_next': round((player.xp / player.xp_for_next_level()) * 100, 1)
        }

    def _get_skills_stats(self, skills: List[Skill]) -> Dict:
        """Skills statistics"""
        if not skills:
            return {'total': 0}

        total_levels = sum(s.level for s in skills)
        avg_level = total_levels / len(skills)
        ready_skills = sum(1 for s in skills if s.is_ready())
        focus_skills = sum(1 for s in skills if s.is_focus)

        highest = max(skills, key=lambda s: s.level)
        lowest = min(skills, key=lambda s: s.level)

        return {
            'total': len(skills),
            'total_levels': total_levels,
            'average_level': round(avg_level, 2),
            'ready_skills': ready_skills,
            'focus_skills': focus_skills,
            'highest_skill': {
                'name': highest.name,
                'level': highest.level
            },
            'lowest_skill': {
                'name': lowest.name,
                'level': lowest.level
            },
            'level_gap': highest.level - lowest.level
        }

    def _get_missions_stats(self, missions: List[Mission]) -> Dict:
        """Missions statistics"""
        if not missions:
            return {'total': 0}

        difficulties = [m.difficulty for m in missions]
        energies = [m.energy for m in missions]

        return {
            'total': len(missions),
            'avg_difficulty': round(sum(difficulties) / len(difficulties), 2),
            'avg_energy': round(sum(energies) / len(energies), 2),
            'difficulty_distribution': {
                str(i): sum(1 for d in difficulties if d == i)
                for i in range(1, 6)
            },
            'energy_distribution': {
                str(i): sum(1 for e in energies if e == i)
                for i in range(1, 6)
            }
        }

    def _get_journal_stats(self, entries: List) -> Dict:
        """Journal statistics"""
        reflections = [e for e in entries if e.is_reflection_token]

        return {
            'total_entries': len(entries),
            'reflections': len(reflections),
            'freeform_entries': len(entries) - len(reflections),
            'avg_per_week': round(len(entries) / max(1, (datetime.now() - entries[-1].created_at if entries else datetime.now()).days / 7), 1) if entries else 0
        }

    def _get_goals_stats(self, goals: List) -> Dict:
        """Goals statistics"""
        if not goals:
            return {'total': 0}

        active = sum(1 for g in goals if g.status.value == 'active')
        completed = sum(1 for g in goals if g.status.value == 'completed')

        completion_rate = (completed / len(goals)) * 100 if goals else 0

        return {
            'total': len(goals),
            'active': active,
            'completed': completed,
            'completion_rate': round(completion_rate, 1)
        }

    def _get_streaks_stats(self, streaks: List) -> Dict:
        """Streaks statistics"""
        if not streaks:
            return {}

        overall = next((s for s in streaks if s.skill_id is None), None)
        active_streaks = sum(1 for s in streaks if s.is_active(date.today()))

        longest_ever = max(streaks, key=lambda s: s.longest_streak)

        return {
            'overall_current': overall.current_streak if overall else 0,
            'overall_longest': overall.longest_streak if overall else 0,
            'active_streaks': active_streaks,
            'longest_streak_ever': {
                'value': longest_ever.longest_streak,
                'skill_id': longest_ever.skill_id
            }
        }

    def _get_economy_stats(self, player: Optional[Player], rewards: List, redemptions: List) -> Dict:
        """Economy statistics"""
        if not player:
            return {}

        total_spent = sum(r.coins_spent for r in redemptions)
        total_earned = player.coins + total_spent

        return {
            'current_coins': player.coins,
            'total_earned': total_earned,
            'total_spent': total_spent,
            'redemptions_count': len(redemptions),
            'available_rewards': len(rewards),
            'avg_redemption': round(total_spent / len(redemptions), 1) if redemptions else 0
        }

    def _get_timeline_stats(self) -> Dict:
        """Timeline statistics (last 7, 30, 90 days)"""
        # This would require tracking completions over time
        # Simplified for now
        return {
            'last_7_days': {},
            'last_30_days': {},
            'last_90_days': {}
        }

    def _get_trends_stats(self) -> Dict:
        """Trend analysis"""
        # This would analyze changes over time
        # Simplified for now
        return {
            'xp_trend': 'stable',
            'activity_trend': 'stable'
        }

    def get_skill_history(self, skill_id: str) -> Dict[str, any]:
        """
        Get detailed history for a skill.

        Args:
            skill_id: Skill to analyze

        Returns:
            Dict with skill history
        """
        skill = self.storage.get_skill(skill_id)
        if not skill:
            return {}

        cycle_history = self.storage.get_cycle_history(skill_id, limit=20)

        hit_rate = sum(1 for h in cycle_history if h['target_hit']) / len(cycle_history) if cycle_history else 0

        return {
            'current_level': skill.level,
            'current_xp': skill.xp,
            'is_focus': skill.is_focus,
            'is_ready': skill.is_ready(),
            'cycle_history': cycle_history,
            'cycle_hit_rate': round(hit_rate * 100, 1),
            'total_cycles': len(cycle_history)
        }

    def generate_text_charts(self, stats: Dict[str, any]) -> Dict[str, str]:
        """
        Generate ASCII/text-based charts from statistics.

        Args:
            stats: Statistics data

        Returns:
            Dict of chart type -> text chart
        """
        charts = {}

        # Difficulty distribution bar chart
        if 'missions' in stats and 'difficulty_distribution' in stats['missions']:
            dist = stats['missions']['difficulty_distribution']
            max_val = max(dist.values()) if dist.values() else 1

            lines = ["Mission Difficulty Distribution:", ""]
            for level, count in dist.items():
                bar_length = int((count / max_val) * 30)
                bar = "█" * bar_length
                lines.append(f"Lvl {level}: {bar} ({count})")

            charts['difficulty_distribution'] = "\n".join(lines)

        # Skills level chart
        if 'skills' in stats:
            skills = self.storage.get_skills(include_archived=False)
            if skills:
                max_level = max(s.level for s in skills)
                lines = ["Skill Levels:", ""]
                for skill in sorted(skills, key=lambda s: s.level, reverse=True):
                    bar_length = int((skill.level / max_level) * 30)
                    bar = "█" * bar_length
                    focus_marker = "⭐" if skill.is_focus else ""
                    lines.append(f"{skill.name[:15]:15} {bar} Lvl {skill.level} {focus_marker}")

                charts['skill_levels'] = "\n".join(lines)

        return charts

"""Data visualization service - generate charts and graphs for export"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from ..services import StorageService, StatisticsService


class VisualizationService:
    """
    Generate visualizations for data export.
    Creates chart data in formats suitable for web/terminal rendering.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage
        self.stats = StatisticsService(storage)

    def generate_all_visualizations(self) -> Dict[str, any]:
        """
        Generate all available visualizations.

        Returns:
            Dict with visualization data
        """
        stats = self.stats.get_comprehensive_stats()

        return {
            'charts': {
                'skill_levels_bar': self._create_skill_levels_chart(),
                'difficulty_distribution_pie': self._create_difficulty_pie(),
                'xp_progress_line': self._create_xp_progress_line(),
                'cycle_performance_bar': self._create_cycle_performance(),
                'goal_progress_gauge': self._create_goals_progress(),
                'streak_timeline': self._create_streak_timeline(),
                'coin_flow': self._create_coin_flow(),
            },
            'text_charts': self.stats.generate_text_charts(stats),
            'stats_summary': stats
        }

    def _create_skill_levels_chart(self) -> Dict:
        """Bar chart of skill levels"""
        skills = self.storage.get_skills(include_archived=False)

        return {
            'type': 'bar',
            'title': 'Skill Levels',
            'labels': [s.name for s in skills],
            'data': [s.level for s in skills],
            'colors': [s.color for s in skills],
            'metadata': {
                'focus_skills': [s.name for s in skills if s.is_focus],
                'ready_skills': [s.name for s in skills if s.is_ready()]
            }
        }

    def _create_difficulty_pie(self) -> Dict:
        """Pie chart of mission difficulty distribution"""
        missions = self.storage.get_missions(include_archived=False)

        distribution = {}
        for mission in missions:
            distribution[mission.difficulty] = distribution.get(mission.difficulty, 0) + 1

        return {
            'type': 'pie',
            'title': 'Mission Difficulty Distribution',
            'labels': [f"Level {d}" for d in sorted(distribution.keys())],
            'data': [distribution[d] for d in sorted(distribution.keys())],
            'colors': ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
        }

    def _create_xp_progress_line(self) -> Dict:
        """Line chart of XP progress over time"""
        player = self.storage.get_player()
        skills = self.storage.get_skills(include_archived=False)

        # For now, show current state
        # In a full implementation, this would track XP over time
        return {
            'type': 'line',
            'title': 'XP Progress',
            'datasets': [
                {
                    'label': 'Player XP',
                    'data': [player.xp] if player else [0],
                    'color': '#2196F3'
                },
                *[
                    {
                        'label': f"{s.name} XP",
                        'data': [s.xp],
                        'color': s.color
                    }
                    for s in skills[:5]  # Limit to 5 skills for clarity
                ]
            ]
        }

    def _create_cycle_performance(self) -> Dict:
        """Bar chart of cycle hit rate per skill"""
        skills = self.storage.get_skills(include_archived=False)

        labels = []
        data = []
        colors = []

        for skill in skills:
            history = self.storage.get_cycle_history(skill.id, limit=10)
            if history:
                hit_rate = sum(1 for h in history if h['target_hit']) / len(history)
                labels.append(skill.name)
                data.append(round(hit_rate * 100, 1))
                colors.append(skill.color)

        return {
            'type': 'bar',
            'title': 'Cycle Target Hit Rate (%)',
            'labels': labels,
            'data': data,
            'colors': colors
        }

    def _create_goals_progress(self) -> Dict:
        """Gauge chart for goals progress"""
        goals = self.storage.get_goals(status='active')

        gauges = []
        for goal in goals:
            gauges.append({
                'title': goal.title,
                'current': goal.current_value,
                'target': goal.target_value,
                'percentage': goal.progress_percentage(),
                'type': goal.goal_type.value
            })

        return {
            'type': 'gauges',
            'title': 'Goals Progress',
            'gauges': gauges
        }

    def _create_streak_timeline(self) -> Dict:
        """Timeline visualization of streaks"""
        streaks = self.storage.get_streaks()

        timeline_data = []
        for streak in streaks:
            skill_name = "Overall" if streak.skill_id is None else "Skill"
            timeline_data.append({
                'skill': skill_name,
                'current_streak': streak.current_streak,
                'longest_streak': streak.longest_streak,
                'last_date': streak.last_completion_date.isoformat() if streak.last_completion_date else None
            })

        return {
            'type': 'timeline',
            'title': 'Streak Status',
            'data': timeline_data
        }

    def _create_coin_flow(self) -> Dict:
        """Sankey/flow diagram of coin earning and spending"""
        player = self.storage.get_player()
        redemptions = self.storage.get_redemptions(limit=100)

        total_spent = sum(r.coins_spent for r in redemptions)
        total_earned = (player.coins if player else 0) + total_spent

        return {
            'type': 'flow',
            'title': 'Coin Economy',
            'nodes': [
                {'name': 'Missions', 'value': total_earned},
                {'name': 'Current Balance', 'value': player.coins if player else 0},
                {'name': 'Rewards', 'value': total_spent}
            ],
            'links': [
                {'source': 'Missions', 'target': 'Current Balance', 'value': player.coins if player else 0},
                {'source': 'Missions', 'target': 'Rewards', 'value': total_spent}
            ]
        }

    def export_for_web_dashboard(self) -> str:
        """
        Export visualization data in HTML format.

        Returns:
            HTML string with embedded Chart.js visualizations
        """
        viz_data = self.generate_all_visualizations()

        html = """
<!DOCTYPE html>
<html>
<head>
    <title>New Game Plus - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
        }
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #4ecca3;
            font-size: 2.5em;
            margin-bottom: 40px;
        }
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .chart-container {
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .chart-title {
            color: #4ecca3;
            font-size: 1.3em;
            margin-bottom: 15px;
            text-align: center;
        }
        canvas {
            max-height: 300px;
        }
        .stats-summary {
            background: #16213e;
            border-radius: 10px;
            padding: 30px;
            margin-top: 30px;
        }
        .stat-card {
            display: inline-block;
            background: #0f3460;
            padding: 15px 25px;
            margin: 10px;
            border-radius: 8px;
            border-left: 4px solid #4ecca3;
        }
        .stat-label {
            color: #aaa;
            font-size: 0.9em;
        }
        .stat-value {
            color: #4ecca3;
            font-size: 1.8em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>✨ New Game Plus Dashboard ✨</h1>

        <div class="chart-grid">
"""

        # Add skill levels chart
        skill_chart = viz_data['charts']['skill_levels_bar']
        if skill_chart['data']:
            html += f"""
            <div class="chart-container">
                <div class="chart-title">{skill_chart['title']}</div>
                <canvas id="skillLevelsChart"></canvas>
            </div>
"""

        # Add difficulty distribution
        diff_chart = viz_data['charts']['difficulty_distribution_pie']
        html += f"""
            <div class="chart-container">
                <div class="chart-title">{diff_chart['title']}</div>
                <canvas id="difficultyChart"></canvas>
            </div>
"""

        html += """
        </div>

        <div class="stats-summary">
            <h2 style="color: #4ecca3; margin-bottom: 20px;">Quick Stats</h2>
"""

        # Add stats cards
        stats = viz_data['stats_summary']
        if 'player' in stats:
            p = stats['player']
            html += f"""
            <div class="stat-card">
                <div class="stat-label">Level</div>
                <div class="stat-value">{p.get('level', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total XP</div>
                <div class="stat-value">{p.get('total_xp', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Coins</div>
                <div class="stat-value">{p.get('coins', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Days Playing</div>
                <div class="stat-value">{p.get('days_playing', 0)}</div>
            </div>
"""

        html += """
        </div>
    </div>

    <script>
"""

        # Add Chart.js initialization
        if skill_chart['data']:
            html += f"""
        new Chart(document.getElementById('skillLevelsChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(skill_chart['labels'])},
                datasets: [{{
                    label: 'Level',
                    data: {json.dumps(skill_chart['data'])},
                    backgroundColor: {json.dumps(skill_chart['colors'])}
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ color: '#eee' }} }},
                    x: {{ ticks: {{ color: '#eee' }} }}
                }}
            }}
        }});
"""

        html += f"""
        new Chart(document.getElementById('difficultyChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(diff_chart['labels'])},
                datasets: [{{
                    data: {json.dumps(diff_chart['data'])},
                    backgroundColor: {json.dumps(diff_chart['colors'])}
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ labels: {{ color: '#eee' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

        return html

    def export_visualization_data(self) -> Dict:
        """
        Export raw visualization data for external tools.

        Returns:
            Dict with all chart data in standard format
        """
        return self.generate_all_visualizations()

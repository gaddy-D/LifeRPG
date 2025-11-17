"""Dashboard - main UI view for New Game Plus"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from typing import List, Optional
from ..models import Player, Skill, Mission
from ..loops import SuggestionLoop
from ..services import ProgressionService


class Dashboard:
    """Main dashboard view"""

    def __init__(self, console: Console):
        self.console = console
        self.progression = ProgressionService()

    def render(
        self,
        player: Player,
        skills: List[Skill],
        missions: List[Mission],
        suggestion_loop: SuggestionLoop
    ):
        """Render the main dashboard"""
        self.console.clear()

        # Title
        title = Text("✨ NEW GAME PLUS ✨", style="bold magenta", justify="center")
        self.console.print(title)
        self.console.print()

        # Player info
        self._render_player_info(player)
        self.console.print()

        # Skills overview
        self._render_skills(skills)
        self.console.print()

        # Missions preview
        self._render_missions_preview(missions)
        self.console.print()

        # Navigator suggestions
        self._render_suggestions(suggestion_loop)
        self.console.print()

    def _render_player_info(self, player: Player):
        """Render player stats"""
        progress = self.progression.get_player_progress_display(player)

        # Progress bar
        xp_bar = self._create_progress_bar(
            progress['xp'],
            progress['xp_needed'],
            width=30
        )

        info = Table.grid(padding=(0, 2))
        info.add_column(style="cyan", justify="right")
        info.add_column()

        info.add_row("Class:", f"[bold]{player.class_name}[/bold]")
        info.add_row("Name:", player.display_name)
        info.add_row("Level:", f"[bold yellow]{progress['level']}[/bold yellow]")
        info.add_row("XP:", f"{xp_bar} {progress['xp']}/{progress['xp_needed']}")
        info.add_row("Coins:", f"[bold gold1]{progress['coins']}[/bold gold1] 💰")

        panel = Panel(info, title="Character", border_style="cyan")
        self.console.print(panel)

    def _render_skills(self, skills: List[Skill]):
        """Render skills table"""
        table = Table(title="Skills", border_style="blue")

        table.add_column("Skill", style="cyan", no_wrap=True)
        table.add_column("Level", justify="center")
        table.add_column("Progress", justify="left")
        table.add_column("Ready", justify="center")
        table.add_column("Cycle", justify="center")
        table.add_column("Focus", justify="center")

        for skill in skills:
            progress = self.progression.get_skill_progress_display(skill)

            # Progress bar
            xp_bar = self._create_progress_bar(
                progress['xp'],
                progress['xp_needed'],
                width=15
            )

            # Readiness indicator
            ready_icon = "✓" if skill.is_ready() else "✗"
            ready_style = "green" if skill.is_ready() else "red"

            # Cycle status
            cycle_icon = "⚡" if skill.has_hit_target_this_cycle else "○"
            cycle_style = "yellow" if skill.has_hit_target_this_cycle else "dim"

            # Focus indicator
            focus = "⭐" if skill.is_focus else ""

            table.add_row(
                f"{skill.icon_key} {skill.name}",
                f"[bold]{progress['level']}[/bold]",
                f"{xp_bar} {progress['xp']}/{progress['xp_needed']}",
                f"[{ready_style}]{ready_icon}[/{ready_style}] {skill.readiness_display()}",
                f"[{cycle_style}]{cycle_icon}[/{cycle_style}]",
                focus
            )

        self.console.print(table)

    def _render_missions_preview(self, missions: List[Mission], limit: int = 5):
        """Render preview of available missions"""
        table = Table(title=f"Available Missions (showing {min(limit, len(missions))} of {len(missions)})", border_style="green")

        table.add_column("Mission", style="green")
        table.add_column("Difficulty", justify="center")
        table.add_column("Energy", justify="center")

        for mission in missions[:limit]:
            diff_stars = "★" * mission.difficulty
            energy_dots = "●" * mission.energy

            table.add_row(
                mission.title,
                diff_stars,
                energy_dots
            )

        self.console.print(table)

    def _render_suggestions(self, suggestion_loop: SuggestionLoop):
        """Render Navigator suggestions"""
        suggestions = suggestion_loop.generate_suggestions(max_suggestions=2)

        if not suggestions:
            return

        for suggestion in suggestions:
            style = {
                "high": "red",
                "normal": "yellow",
                "low": "blue"
            }.get(suggestion.priority, "white")

            message = f"[bold]{suggestion.title}[/bold]\n{suggestion.message}"
            if suggestion.action_hint:
                message += f"\n[dim]{suggestion.action_hint}[/dim]"

            panel = Panel(message, border_style=style, title="💡 Navigator")
            self.console.print(panel)

    def _create_progress_bar(self, current: int, total: int, width: int = 20) -> str:
        """Create a text-based progress bar"""
        if total == 0:
            percentage = 0
        else:
            percentage = min(1.0, current / total)

        filled = int(width * percentage)
        bar = "█" * filled + "░" * (width - filled)
        return f"[cyan]{bar}[/cyan]"

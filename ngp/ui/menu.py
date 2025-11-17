"""Menu system for New Game Plus"""

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Optional, List, Callable
import uuid
from ..models import Player, Skill, Mission
from ..models.skill import CycleType
from ..loops import *
from ..services import StorageService


class Menu:
    """Interactive menu system"""

    def __init__(self, console: Console, storage: StorageService):
        self.console = console
        self.storage = storage

    def show_main_menu(self) -> Optional[str]:
        """
        Show main menu and return selected option.

        Returns:
            Selected menu option or None to quit
        """
        self.console.print("\n[bold cyan]═══ MAIN MENU ═══[/bold cyan]")
        self.console.print("1. Complete a Mission")
        self.console.print("2. Create New Mission")
        self.console.print("3. Manage Skills")
        self.console.print("4. Journal & Reflections")
        self.console.print("5. View Navigator Insights")
        self.console.print("6. Adjustments")
        self.console.print("7. Profile")
        self.console.print("0. Quit")

        choice = Prompt.ask("\nChoose an option", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="1")
        return choice if choice != "0" else None

    def select_mission(self, missions: List[Mission]) -> Optional[Mission]:
        """
        Show mission selection menu.

        Returns:
            Selected Mission or None
        """
        if not missions:
            self.console.print("[yellow]No missions available. Create some first![/yellow]")
            return None

        table = Table(title="Select a Mission", border_style="green")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Mission", style="green")
        table.add_column("Diff", justify="center")
        table.add_column("Energy", justify="center")

        for idx, mission in enumerate(missions, 1):
            table.add_row(
                str(idx),
                mission.title,
                "★" * mission.difficulty,
                "●" * mission.energy
            )

        self.console.print(table)

        max_choice = len(missions)
        choice = IntPrompt.ask(
            f"Select mission (1-{max_choice}), or 0 to cancel",
            default=0
        )

        if choice < 1 or choice > max_choice:
            return None

        return missions[choice - 1]

    def create_mission_wizard(self, skills: List[Skill]) -> Optional[dict]:
        """
        Wizard for creating a new mission.

        Returns:
            Dict with mission data, or None if cancelled
        """
        self.console.print("\n[bold cyan]═══ CREATE NEW MISSION ═══[/bold cyan]")

        title = Prompt.ask("Mission title")
        if not title:
            return None

        note = Prompt.ask("Notes (optional)", default="")

        # Select skills (1-2)
        if not skills:
            self.console.print("[yellow]No skills available. Please create a skill first.[/yellow]")
            return None

        table = Table(border_style="blue")
        table.add_column("#", justify="right")
        table.add_column("Skill", style="cyan")
        table.add_column("Level", justify="center")

        for idx, skill in enumerate(skills, 1):
            table.add_row(str(idx), f"{skill.icon_key} {skill.name}", str(skill.level))

        self.console.print(table)

        skill_choices = Prompt.ask(
            "Assign to skill(s) (enter numbers separated by commas, max 2)",
            default="1"
        )

        skill_indices = [int(x.strip()) - 1 for x in skill_choices.split(",") if x.strip().isdigit()]
        skill_indices = [i for i in skill_indices if 0 <= i < len(skills)][:2]

        if not skill_indices:
            self.console.print("[red]No valid skills selected. Cancelled.[/red]")
            return None

        skill_ids = [skills[i].id for i in skill_indices]

        difficulty = IntPrompt.ask("Difficulty (1-5)", default=1)
        difficulty = max(1, min(5, difficulty))

        energy = IntPrompt.ask("Energy (1-5)", default=1)
        energy = max(1, min(5, energy))

        return {
            'title': title,
            'note': note if note else None,
            'skill_ids': skill_ids,
            'difficulty': difficulty,
            'energy': energy
        }

    def create_skill_wizard(self) -> Optional[dict]:
        """
        Wizard for creating a new skill.

        Returns:
            Dict with skill data, or None if cancelled
        """
        self.console.print("\n[bold cyan]═══ CREATE NEW SKILL ═══[/bold cyan]")

        name = Prompt.ask("Skill name (e.g., Writing, Fitness, Coding)")
        if not name:
            return None

        description = Prompt.ask("Description (optional)", default="")

        icon = Prompt.ask("Icon/emoji (optional)", default="⚡")

        # Cycle type
        self.console.print("\nCycle cadence:")
        self.console.print("1. Daily")
        self.console.print("2. Weekly")
        self.console.print("3. Monthly")

        cadence_choice = IntPrompt.ask("Choose cadence", default=2, choices=["1", "2", "3"])
        cycle_type = {
            1: CycleType.DAILY,
            2: CycleType.WEEKLY,
            3: CycleType.MONTHLY
        }[cadence_choice]

        is_focus = Confirm.ask("Make this a Focus skill? (slower leveling, deeper mastery)", default=False)

        return {
            'name': name,
            'description': description if description else None,
            'icon_key': icon,
            'cycle_type': cycle_type,
            'is_focus': is_focus
        }

    def show_journal_menu(self) -> Optional[str]:
        """Show journal submenu"""
        self.console.print("\n[bold cyan]═══ JOURNAL ═══[/bold cyan]")
        self.console.print("1. Write New Entry")
        self.console.print("2. View Recent Entries")
        self.console.print("3. View Reflections Only")
        self.console.print("0. Back")

        return Prompt.ask("Choose an option", choices=["0", "1", "2", "3"], default="2")

    def show_adjustment_menu(self) -> Optional[str]:
        """Show adjustment submenu"""
        self.console.print("\n[bold cyan]═══ ADJUSTMENTS ═══[/bold cyan]")
        self.console.print("1. Change Skill Cadence")
        self.console.print("2. Toggle Focus Mode")
        self.console.print("3. Adjust Mission Difficulty")
        self.console.print("4. Archive Skill")
        self.console.print("5. Archive Mission")
        self.console.print("0. Back")

        return Prompt.ask("Choose an option", choices=["0", "1", "2", "3", "4", "5"], default="0")

    def display_journal_entries(self, entries: List):
        """Display journal entries"""
        if not entries:
            self.console.print("[yellow]No journal entries yet.[/yellow]")
            return

        for entry in entries:
            icon = "💭" if entry.is_reflection_token else "📔"
            entry_type = "Reflection" if entry.is_reflection_token else "Journal"

            header = f"{icon} {entry_type} - {entry.created_at.strftime('%Y-%m-%d %H:%M')}"
            panel = Panel(entry.text, title=header, border_style="blue")
            self.console.print(panel)

    def show_insights(self, insights: List[str]):
        """Display Navigator insights"""
        self.console.print("\n[bold cyan]═══ NAVIGATOR INSIGHTS ═══[/bold cyan]")

        if not insights:
            self.console.print("[dim]No insights available yet. Keep playing to generate patterns![/dim]")
            return

        for insight in insights:
            self.console.print(f"• {insight}")

    def show_completion_result(self, result: dict, mission_title: str):
        """Show mission completion result with rewards"""
        self.console.print()
        panel_content = f"[bold green]Mission Completed:[/bold green] {mission_title}\n\n"
        panel_content += f"[yellow]+{result['xp_earned']} XP[/yellow]\n"
        panel_content += f"[gold1]+{result['coins_earned']} Coins[/gold1]\n"

        if result['cycle_bonus_applied']:
            panel_content += "\n[bold cyan]🎯 CYCLE TARGET HIT! Bonus XP awarded![/bold cyan]"

        if result['player_leveled_up']:
            panel_content += "\n\n[bold magenta]⬆️ LEVEL UP![/bold magenta]"

        if result['skill_level_ups']:
            for skill_name in result['skill_level_ups']:
                panel_content += f"\n[bold blue]⬆️ {skill_name} leveled up![/bold blue]"

        panel = Panel(panel_content, border_style="green", title="✨ Rewards")
        self.console.print(panel)

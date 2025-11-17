#!/usr/bin/env python3
"""
New Game Plus - Main Entry Point

A minimalist offline life RPG system for the Linux terminal.
"""

import uuid
import click
from rich.console import Console
from datetime import datetime
from pathlib import Path

from .models import Player, Skill
from .models.skill import CycleType
from .services import StorageService
from .loops import (
    ActionLoop,
    ReflectionLoop,
    AnalysisLoop,
    SuggestionLoop,
    AdjustmentLoop
)
from .ui import Menu, Dashboard


class GameSession:
    """Main game session manager"""

    def __init__(self, db_path: str = "data/ngp.db"):
        self.console = Console()
        self.storage = StorageService(db_path)

        # Initialize loops
        self.action = ActionLoop(self.storage)
        self.reflection = ReflectionLoop(self.storage)
        self.analysis = AnalysisLoop(self.storage)
        self.suggestion = SuggestionLoop(self.storage)
        self.adjustment = AdjustmentLoop(self.storage)

        # Initialize UI
        self.menu = Menu(self.console, self.storage)
        self.dashboard = Dashboard(self.console)

        # Load or create player
        self.player = self._load_or_create_player()

    def _load_or_create_player(self) -> Player:
        """Load existing player or create new one"""
        player = self.storage.get_player()

        if not player:
            # First time setup
            self.console.print("[bold magenta]✨ Welcome to New Game Plus ✨[/bold magenta]")
            self.console.print("\nLet's create your character.\n")

            display_name = click.prompt("Your name", type=str, default="Player")
            class_name = click.prompt("Your class/role (e.g., Digital Craftsman, Aspiring Artist)", type=str)
            class_description = click.prompt("Class description (optional)", type=str, default="")

            player = Player(
                id=str(uuid.uuid4()),
                display_name=display_name,
                class_name=class_name,
                class_description=class_description if class_description else None
            )

            self.storage.save_player(player)
            self.console.print("\n[green]Character created successfully![/green]")

        return player

    def run(self):
        """Main game loop"""
        running = True

        while running:
            # Refresh data
            skills = self.storage.get_skills(include_archived=False)
            missions = self.storage.get_missions(include_archived=False)

            # Render dashboard
            self.dashboard.render(
                self.player,
                skills,
                missions,
                self.suggestion
            )

            # Show menu
            choice = self.menu.show_main_menu()

            if choice is None:
                # Quit
                running = False
                self.console.print("\n[cyan]Thanks for playing! Your progress is saved.[/cyan]")

            elif choice == "1":
                # Complete a mission
                self._handle_complete_mission(missions)

            elif choice == "2":
                # Create new mission
                self._handle_create_mission(skills)

            elif choice == "3":
                # Manage skills
                self._handle_manage_skills(skills)

            elif choice == "4":
                # Journal
                self._handle_journal()

            elif choice == "5":
                # Navigator insights
                self._handle_insights()

            elif choice == "6":
                # Adjustments
                self._handle_adjustments(skills, missions)

            elif choice == "7":
                # Profile
                self._handle_profile()

    def _handle_complete_mission(self, missions):
        """Handle mission completion"""
        if not missions:
            self.console.print("[yellow]No missions available. Create some first![/yellow]")
            click.pause()
            return

        mission = self.menu.select_mission(missions)
        if not mission:
            return

        try:
            result = self.action.complete_mission(mission.id, self.player)

            # Show rewards
            self.menu.show_completion_result(result, mission.title)

            # Maybe prompt reflection
            skill_id = mission.skill_ids[0] if mission.skill_ids else None
            if self.reflection.should_prompt_reflection(result['completion'], skill_id):
                prompt = self.reflection.get_random_prompt()
                self.console.print(f"\n[italic cyan]{prompt}[/italic cyan]")

                if click.confirm("Would you like to write a reflection?", default=False):
                    reflection_text = click.prompt("Your reflection", type=str)
                    self.reflection.create_reflection(
                        reflection_text,
                        mission_id=mission.id,
                        skill_id=skill_id
                    )
                    self.console.print("[green]Reflection saved.[/green]")

            click.pause()

        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            click.pause()

    def _handle_create_mission(self, skills):
        """Handle mission creation"""
        if not skills:
            self.console.print("[yellow]You need to create at least one skill first![/yellow]")
            if click.confirm("Create a skill now?", default=True):
                self._handle_create_skill()
            return

        mission_data = self.menu.create_mission_wizard(skills)
        if mission_data:
            try:
                mission = self.action.create_mission(**mission_data)
                self.console.print(f"[green]Mission '{mission.title}' created successfully![/green]")
                click.pause()
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                click.pause()

    def _handle_manage_skills(self, skills):
        """Handle skill management"""
        self.console.print("\n[bold cyan]═══ SKILL MANAGEMENT ═══[/bold cyan]")
        self.console.print("1. Create New Skill")
        self.console.print("2. View Skills")
        self.console.print("0. Back")

        choice = click.prompt("Choose option", type=str, default="0")

        if choice == "1":
            self._handle_create_skill()
        elif choice == "2":
            # Skills are shown on dashboard
            click.pause()

    def _handle_create_skill(self):
        """Handle skill creation"""
        skill_data = self.menu.create_skill_wizard()
        if skill_data:
            try:
                skill = Skill(
                    id=str(uuid.uuid4()),
                    **skill_data
                )

                # Initialize cycle
                from datetime import datetime
                missions = []
                from .services import CycleService
                cycle_service = CycleService()
                cycle_service.start_new_cycle(
                    skill,
                    missions,
                    datetime.now(),
                    self.player.day_starts_at
                )

                self.storage.save_skill(skill)
                self.console.print(f"[green]Skill '{skill.name}' created successfully![/green]")
                click.pause()
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                click.pause()

    def _handle_journal(self):
        """Handle journal viewing and creation"""
        while True:
            choice = self.menu.show_journal_menu()

            if choice == "0":
                break

            elif choice == "1":
                # Write new entry
                text = click.prompt("Journal entry", type=str)
                entry = self.reflection.create_journal_entry(text)
                self.console.print("[green]Journal entry saved.[/green]")
                click.pause()

            elif choice == "2":
                # View recent entries
                entries = self.reflection.get_recent_entries(limit=10)
                self.menu.display_journal_entries(entries)
                click.pause()

            elif choice == "3":
                # View reflections only
                reflections = self.reflection.get_reflections_only(limit=10)
                self.menu.display_journal_entries(reflections)
                click.pause()

    def _handle_insights(self):
        """Handle Navigator insights"""
        insights = self.analysis.generate_insights()
        self.menu.show_insights(insights)
        click.pause()

    def _handle_adjustments(self, skills, missions):
        """Handle player adjustments"""
        while True:
            choice = self.menu.show_adjustment_menu()

            if choice == "0":
                break

            elif choice == "1":
                # Change skill cadence
                if not skills:
                    self.console.print("[yellow]No skills available.[/yellow]")
                    click.pause()
                    continue

                # Show skills and let user pick one
                for idx, skill in enumerate(skills, 1):
                    self.console.print(f"{idx}. {skill.name} ({skill.cycle_type.value})")

                skill_idx = click.prompt("Select skill", type=int, default=1) - 1
                if 0 <= skill_idx < len(skills):
                    self.console.print("1. Daily  2. Weekly  3. Monthly")
                    cadence_choice = click.prompt("New cadence", type=int, default=2)
                    new_cadence = {1: CycleType.DAILY, 2: CycleType.WEEKLY, 3: CycleType.MONTHLY}.get(cadence_choice, CycleType.WEEKLY)

                    self.adjustment.change_skill_cadence(
                        skills[skill_idx].id,
                        new_cadence,
                        self.player.day_starts_at
                    )
                    self.console.print("[green]Cadence updated.[/green]")

                click.pause()

            elif choice == "2":
                # Toggle focus mode
                if not skills:
                    self.console.print("[yellow]No skills available.[/yellow]")
                    click.pause()
                    continue

                for idx, skill in enumerate(skills, 1):
                    focus = "⭐ FOCUS" if skill.is_focus else ""
                    self.console.print(f"{idx}. {skill.name} {focus}")

                skill_idx = click.prompt("Select skill", type=int, default=1) - 1
                if 0 <= skill_idx < len(skills):
                    self.adjustment.toggle_focus_mode(skills[skill_idx].id)
                    self.console.print("[green]Focus mode toggled.[/green]")

                click.pause()

    def _handle_profile(self):
        """Handle profile viewing"""
        self.console.print(f"\n[bold cyan]═══ PROFILE ═══[/bold cyan]")
        self.console.print(f"Name: {self.player.display_name}")
        self.console.print(f"Class: {self.player.class_name}")
        if self.player.class_description:
            self.console.print(f"Description: {self.player.class_description}")
        self.console.print(f"Level: {self.player.level}")
        self.console.print(f"XP: {self.player.xp}")
        self.console.print(f"Coins: {self.player.coins}")
        self.console.print(f"Created: {self.player.created_at.strftime('%Y-%m-%d')}")
        click.pause()


@click.command()
@click.option('--db', default="data/ngp.db", help='Path to database file')
def cli(db):
    """
    New Game Plus - A minimalist offline life RPG

    Track missions, develop skills, and level up your real life.
    """
    # Ensure data directory exists
    Path(db).parent.mkdir(parents=True, exist_ok=True)

    # Start game session
    session = GameSession(db_path=db)
    session.run()


if __name__ == "__main__":
    cli()

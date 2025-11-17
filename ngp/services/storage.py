"""Storage service using SQLite for local data persistence"""

import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models import Player, Skill, Mission, Completion, JournalEntry, TimeCapsule
from ..models.skill import CycleType
from ..models.mission import ScheduleType
from ..models.completion import Award
from ..models.capsule import UnlockType


class StorageService:
    """
    Manages local SQLite database for all game data.
    Single-user, offline-first design.
    """

    def __init__(self, db_path: str = "data/ngp.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Initialize database with schema"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Access columns by name

        cursor = self.conn.cursor()

        # Player table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                class_description TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                day_starts_at INTEGER DEFAULT 0
            )
        """)

        # Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#3B82F6',
                icon_key TEXT DEFAULT '⚡',
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                is_archived BOOLEAN DEFAULT 0,
                is_focus BOOLEAN DEFAULT 0,
                order_idx INTEGER DEFAULT 0,
                cycle_type TEXT DEFAULT 'weekly',
                cycle_start TEXT,
                cycle_end TEXT,
                target_mission_id TEXT,
                has_hit_target_this_cycle BOOLEAN DEFAULT 0,
                missions_count INTEGER DEFAULT 0
            )
        """)

        # Missions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                note TEXT,
                skill_ids TEXT,  -- JSON array
                difficulty INTEGER DEFAULT 1,
                energy INTEGER DEFAULT 1,
                schedule TEXT DEFAULT 'one_off',
                due_at TEXT,
                is_archived BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Completions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id TEXT PRIMARY KEY,
                mission_id TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                award_data TEXT NOT NULL,  -- JSON
                cycle_id TEXT NOT NULL,
                reflection_requested BOOLEAN DEFAULT 0,
                FOREIGN KEY (mission_id) REFERENCES missions(id)
            )
        """)

        # Journal entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                text TEXT NOT NULL,
                skill_id TEXT,
                mission_id TEXT,
                is_reflection_token BOOLEAN DEFAULT 0,
                edited_at TEXT
            )
        """)

        # Time capsules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time_capsules (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_encrypted BOOLEAN DEFAULT 0,
                passphrase_hint TEXT,
                unlock_type TEXT NOT NULL,
                unlock_params TEXT NOT NULL,  -- JSON
                unlocked_at TEXT,
                archived_to_journal_entry_id TEXT
            )
        """)

        self.conn.commit()

    # Player methods
    def get_player(self) -> Optional[Player]:
        """Get the player (single-user game)"""
        cursor = self.conn.cursor()
        row = cursor.execute("SELECT * FROM player LIMIT 1").fetchone()
        if not row:
            return None

        return Player(
            id=row['id'],
            display_name=row['display_name'],
            class_name=row['class_name'],
            class_description=row['class_description'],
            level=row['level'],
            xp=row['xp'],
            coins=row['coins'],
            created_at=datetime.fromisoformat(row['created_at']),
            day_starts_at=row['day_starts_at']
        )

    def save_player(self, player: Player):
        """Save or update player"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO player
            (id, display_name, class_name, class_description, level, xp, coins, created_at, day_starts_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player.id,
            player.display_name,
            player.class_name,
            player.class_description,
            player.level,
            player.xp,
            player.coins,
            player.created_at.isoformat(),
            player.day_starts_at
        ))
        self.conn.commit()

    # Skill methods
    def get_skills(self, include_archived: bool = False) -> List[Skill]:
        """Get all skills"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM skills"
        if not include_archived:
            query += " WHERE is_archived = 0"
        query += " ORDER BY order_idx"

        rows = cursor.execute(query).fetchall()
        return [self._row_to_skill(row) for row in rows]

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get specific skill"""
        cursor = self.conn.cursor()
        row = cursor.execute("SELECT * FROM skills WHERE id = ?", (skill_id,)).fetchone()
        return self._row_to_skill(row) if row else None

    def save_skill(self, skill: Skill):
        """Save or update skill"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO skills
            (id, name, description, color, icon_key, level, xp, is_archived, is_focus,
             order_idx, cycle_type, cycle_start, cycle_end, target_mission_id,
             has_hit_target_this_cycle, missions_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            skill.id,
            skill.name,
            skill.description,
            skill.color,
            skill.icon_key,
            skill.level,
            skill.xp,
            skill.is_archived,
            skill.is_focus,
            skill.order,
            skill.cycle_type.value,
            skill.cycle_start.isoformat() if skill.cycle_start else None,
            skill.cycle_end.isoformat() if skill.cycle_end else None,
            skill.target_mission_id,
            skill.has_hit_target_this_cycle,
            skill.missions_count
        ))
        self.conn.commit()

    def _row_to_skill(self, row) -> Skill:
        """Convert DB row to Skill object"""
        return Skill(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            color=row['color'],
            icon_key=row['icon_key'],
            level=row['level'],
            xp=row['xp'],
            is_archived=bool(row['is_archived']),
            is_focus=bool(row['is_focus']),
            order=row['order_idx'],
            cycle_type=CycleType(row['cycle_type']),
            cycle_start=datetime.fromisoformat(row['cycle_start']) if row['cycle_start'] else None,
            cycle_end=datetime.fromisoformat(row['cycle_end']) if row['cycle_end'] else None,
            target_mission_id=row['target_mission_id'],
            has_hit_target_this_cycle=bool(row['has_hit_target_this_cycle']),
            missions_count=row['missions_count']
        )

    # Mission methods
    def get_missions(self, include_archived: bool = False) -> List[Mission]:
        """Get all missions"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM missions"
        if not include_archived:
            query += " WHERE is_archived = 0"
        query += " ORDER BY created_at DESC"

        rows = cursor.execute(query).fetchall()
        return [self._row_to_mission(row) for row in rows]

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Get specific mission"""
        cursor = self.conn.cursor()
        row = cursor.execute("SELECT * FROM missions WHERE id = ?", (mission_id,)).fetchone()
        return self._row_to_mission(row) if row else None

    def save_mission(self, mission: Mission):
        """Save or update mission"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO missions
            (id, title, note, skill_ids, difficulty, energy, schedule, due_at,
             is_archived, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mission.id,
            mission.title,
            mission.note,
            json.dumps(mission.skill_ids),
            mission.difficulty,
            mission.energy,
            mission.schedule.value,
            mission.due_at.isoformat() if mission.due_at else None,
            mission.is_archived,
            mission.created_at.isoformat(),
            mission.updated_at.isoformat()
        ))
        self.conn.commit()

    def _row_to_mission(self, row) -> Mission:
        """Convert DB row to Mission object"""
        return Mission(
            id=row['id'],
            title=row['title'],
            note=row['note'],
            skill_ids=json.loads(row['skill_ids']),
            difficulty=row['difficulty'],
            energy=row['energy'],
            schedule=ScheduleType(row['schedule']),
            due_at=datetime.fromisoformat(row['due_at']) if row['due_at'] else None,
            is_archived=bool(row['is_archived']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )

    # Completion methods
    def save_completion(self, completion: Completion):
        """Save a completion"""
        cursor = self.conn.cursor()
        award_data = {
            'base_player_xp': completion.award.base_player_xp,
            'base_skill_xp_map': completion.award.base_skill_xp_map,
            'coins': completion.award.coins,
            'cycle_xp_applied_skill_id': completion.award.cycle_xp_applied_skill_id
        }

        cursor.execute("""
            INSERT INTO completions
            (id, mission_id, completed_at, award_data, cycle_id, reflection_requested)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            completion.id,
            completion.mission_id,
            completion.completed_at.isoformat(),
            json.dumps(award_data),
            completion.cycle_id,
            completion.reflection_requested
        ))
        self.conn.commit()

    def get_completions_for_mission_in_cycle(self, mission_id: str, cycle_id: str) -> List[Completion]:
        """Check if mission was completed in this cycle"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT * FROM completions
            WHERE mission_id = ? AND cycle_id = ?
        """, (mission_id, cycle_id)).fetchall()
        return [self._row_to_completion(row) for row in rows]

    def _row_to_completion(self, row) -> Completion:
        """Convert DB row to Completion object"""
        award_data = json.loads(row['award_data'])
        return Completion(
            id=row['id'],
            mission_id=row['mission_id'],
            completed_at=datetime.fromisoformat(row['completed_at']),
            award=Award(
                base_player_xp=award_data['base_player_xp'],
                base_skill_xp_map=award_data['base_skill_xp_map'],
                coins=award_data['coins'],
                cycle_xp_applied_skill_id=award_data.get('cycle_xp_applied_skill_id')
            ),
            cycle_id=row['cycle_id'],
            reflection_requested=bool(row['reflection_requested'])
        )

    # Journal methods
    def save_journal_entry(self, entry: JournalEntry):
        """Save journal entry"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO journal_entries
            (id, created_at, text, skill_id, mission_id, is_reflection_token, edited_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.id,
            entry.created_at.isoformat(),
            entry.text,
            entry.skill_id,
            entry.mission_id,
            entry.is_reflection_token,
            entry.edited_at.isoformat() if entry.edited_at else None
        ))
        self.conn.commit()

    def get_journal_entries(self, limit: int = 50) -> List[JournalEntry]:
        """Get recent journal entries"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT * FROM journal_entries
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [self._row_to_journal_entry(row) for row in rows]

    def _row_to_journal_entry(self, row) -> JournalEntry:
        """Convert DB row to JournalEntry object"""
        return JournalEntry(
            id=row['id'],
            created_at=datetime.fromisoformat(row['created_at']),
            text=row['text'],
            skill_id=row['skill_id'],
            mission_id=row['mission_id'],
            is_reflection_token=bool(row['is_reflection_token']),
            edited_at=datetime.fromisoformat(row['edited_at']) if row['edited_at'] else None
        )

    # Time Capsule methods
    def save_capsule(self, capsule: TimeCapsule):
        """Save time capsule"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO time_capsules
            (id, title, body, created_at, is_encrypted, passphrase_hint,
             unlock_type, unlock_params, unlocked_at, archived_to_journal_entry_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            capsule.id,
            capsule.title,
            capsule.body,
            capsule.created_at.isoformat(),
            capsule.is_encrypted,
            capsule.passphrase_hint,
            capsule.unlock_type.value,
            json.dumps(capsule.unlock_params),
            capsule.unlocked_at.isoformat() if capsule.unlocked_at else None,
            capsule.archived_to_journal_entry_id
        ))
        self.conn.commit()

    def get_unlocked_capsules(self) -> List[TimeCapsule]:
        """Get all unlocked capsules"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT * FROM time_capsules
            WHERE unlocked_at IS NOT NULL
            ORDER BY unlocked_at DESC
        """).fetchall()
        return [self._row_to_capsule(row) for row in rows]

    def get_locked_capsules(self) -> List[TimeCapsule]:
        """Get all locked capsules"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT * FROM time_capsules
            WHERE unlocked_at IS NULL
            ORDER BY created_at DESC
        """).fetchall()
        return [self._row_to_capsule(row) for row in rows]

    def _row_to_capsule(self, row) -> TimeCapsule:
        """Convert DB row to TimeCapsule object"""
        return TimeCapsule(
            id=row['id'],
            title=row['title'],
            body=row['body'],
            created_at=datetime.fromisoformat(row['created_at']),
            is_encrypted=bool(row['is_encrypted']),
            passphrase_hint=row['passphrase_hint'],
            unlock_type=UnlockType(row['unlock_type']),
            unlock_params=json.loads(row['unlock_params']),
            unlocked_at=datetime.fromisoformat(row['unlocked_at']) if row['unlocked_at'] else None,
            archived_to_journal_entry_id=row['archived_to_journal_entry_id']
        )

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

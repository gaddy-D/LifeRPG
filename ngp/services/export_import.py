"""Export/Import service - backup and restore game data"""

import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from ..services import StorageService


class ExportImportService:
    """
    Handles exporting and importing game data.
    Supports JSON export with optional compression.
    """

    VERSION = "1.1.0"

    def __init__(self, storage: StorageService):
        self.storage = storage

    def export_to_file(
        self,
        filepath: str,
        compress: bool = True,
        include_archived: bool = False
    ) -> Dict[str, Any]:
        """
        Export all game data to a file.

        Args:
            filepath: Path to export file
            compress: Whether to gzip compress the output
            include_archived: Whether to include archived items

        Returns:
            Export stats dict
        """
        data = self.export_to_dict(include_archived=include_archived)

        # Convert to JSON
        json_str = json.dumps(data, indent=2, default=str)

        # Save to file
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        if compress:
            with gzip.open(filepath, 'wt', encoding='utf-8') as f:
                f.write(json_str)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)

        return {
            'filepath': filepath,
            'size_bytes': path.stat().st_size,
            'compressed': compress,
            'timestamp': datetime.now().isoformat(),
            'stats': data['stats']
        }

    def export_to_dict(self, include_archived: bool = False) -> Dict[str, Any]:
        """
        Export all game data to a dictionary.

        Args:
            include_archived: Whether to include archived items

        Returns:
            Dict with all game data
        """
        # Get player
        player = self.storage.get_player()

        # Get skills
        skills = self.storage.get_skills(include_archived=include_archived)

        # Get missions
        missions = self.storage.get_missions(include_archived=include_archived)

        # Get journal entries
        journal_entries = self.storage.get_journal_entries(limit=10000)

        # Get capsules
        locked_capsules = self.storage.get_locked_capsules()
        unlocked_capsules = self.storage.get_unlocked_capsules()

        # Build export data
        data = {
            'version': self.VERSION,
            'exported_at': datetime.now().isoformat(),
            'player': self._serialize_player(player) if player else None,
            'skills': [self._serialize_skill(s) for s in skills],
            'missions': [self._serialize_mission(m) for m in missions],
            'journal_entries': [self._serialize_journal_entry(e) for e in journal_entries],
            'capsules': {
                'locked': [self._serialize_capsule(c) for c in locked_capsules],
                'unlocked': [self._serialize_capsule(c) for c in unlocked_capsules]
            },
            'stats': {
                'skills_count': len(skills),
                'missions_count': len(missions),
                'journal_entries_count': len(journal_entries),
                'capsules_count': len(locked_capsules) + len(unlocked_capsules)
            }
        }

        return data

    def import_from_file(
        self,
        filepath: str,
        merge: bool = False
    ) -> Dict[str, Any]:
        """
        Import game data from a file.

        Args:
            filepath: Path to import file
            merge: If True, merge with existing data. If False, replace.

        Returns:
            Import stats dict
        """
        # Load file
        path = Path(filepath)

        # Try as gzip first, fall back to plain JSON
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                json_str = f.read()
        except:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_str = f.read()

        data = json.loads(json_str)

        # Validate version
        if data.get('version') != self.VERSION:
            raise ValueError(f"Version mismatch: file is {data.get('version')}, expected {self.VERSION}")

        # Import data
        return self.import_from_dict(data, merge=merge)

    def import_from_dict(
        self,
        data: Dict[str, Any],
        merge: bool = False
    ) -> Dict[str, Any]:
        """
        Import game data from a dictionary.

        Args:
            data: Export data dict
            merge: If True, merge with existing. If False, replace.

        Returns:
            Import stats dict
        """
        stats = {
            'player_imported': False,
            'skills_imported': 0,
            'missions_imported': 0,
            'journal_entries_imported': 0,
            'capsules_imported': 0
        }

        # Import player (only if no existing player or not merging)
        if data.get('player'):
            existing_player = self.storage.get_player()
            if not existing_player or not merge:
                player = self._deserialize_player(data['player'])
                self.storage.save_player(player)
                stats['player_imported'] = True

        # Import skills
        for skill_data in data.get('skills', []):
            skill = self._deserialize_skill(skill_data)
            self.storage.save_skill(skill)
            stats['skills_imported'] += 1

        # Import missions
        for mission_data in data.get('missions', []):
            mission = self._deserialize_mission(mission_data)
            self.storage.save_mission(mission)
            stats['missions_imported'] += 1

        # Import journal entries
        for entry_data in data.get('journal_entries', []):
            entry = self._deserialize_journal_entry(entry_data)
            self.storage.save_journal_entry(entry)
            stats['journal_entries_imported'] += 1

        # Import capsules
        capsules_data = data.get('capsules', {})
        for capsule_data in capsules_data.get('locked', []) + capsules_data.get('unlocked', []):
            capsule = self._deserialize_capsule(capsule_data)
            self.storage.save_capsule(capsule)
            stats['capsules_imported'] += 1

        return stats

    # Serialization methods
    def _serialize_player(self, player) -> Dict:
        return {
            'id': player.id,
            'display_name': player.display_name,
            'class_name': player.class_name,
            'class_description': player.class_description,
            'level': player.level,
            'xp': player.xp,
            'coins': player.coins,
            'created_at': player.created_at.isoformat(),
            'day_starts_at': player.day_starts_at
        }

    def _serialize_skill(self, skill) -> Dict:
        return {
            'id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'color': skill.color,
            'icon_key': skill.icon_key,
            'level': skill.level,
            'xp': skill.xp,
            'is_archived': skill.is_archived,
            'is_focus': skill.is_focus,
            'order': skill.order,
            'cycle_type': skill.cycle_type.value,
            'cycle_start': skill.cycle_start.isoformat() if skill.cycle_start else None,
            'cycle_end': skill.cycle_end.isoformat() if skill.cycle_end else None,
            'target_mission_id': skill.target_mission_id,
            'has_hit_target_this_cycle': skill.has_hit_target_this_cycle,
            'missions_count': skill.missions_count
        }

    def _serialize_mission(self, mission) -> Dict:
        return {
            'id': mission.id,
            'title': mission.title,
            'note': mission.note,
            'skill_ids': mission.skill_ids,
            'difficulty': mission.difficulty,
            'energy': mission.energy,
            'schedule': mission.schedule.value,
            'due_at': mission.due_at.isoformat() if mission.due_at else None,
            'is_archived': mission.is_archived,
            'created_at': mission.created_at.isoformat(),
            'updated_at': mission.updated_at.isoformat()
        }

    def _serialize_journal_entry(self, entry) -> Dict:
        return {
            'id': entry.id,
            'created_at': entry.created_at.isoformat(),
            'text': entry.text,
            'skill_id': entry.skill_id,
            'mission_id': entry.mission_id,
            'is_reflection_token': entry.is_reflection_token,
            'edited_at': entry.edited_at.isoformat() if entry.edited_at else None
        }

    def _serialize_capsule(self, capsule) -> Dict:
        return {
            'id': capsule.id,
            'title': capsule.title,
            'body': capsule.body,
            'created_at': capsule.created_at.isoformat(),
            'is_encrypted': capsule.is_encrypted,
            'passphrase_hint': capsule.passphrase_hint,
            'unlock_type': capsule.unlock_type.value,
            'unlock_params': capsule.unlock_params,
            'unlocked_at': capsule.unlocked_at.isoformat() if capsule.unlocked_at else None,
            'archived_to_journal_entry_id': capsule.archived_to_journal_entry_id
        }

    # Deserialization methods
    def _deserialize_player(self, data: Dict):
        from ..models import Player
        return Player(
            id=data['id'],
            display_name=data['display_name'],
            class_name=data['class_name'],
            class_description=data.get('class_description'),
            level=data['level'],
            xp=data['xp'],
            coins=data['coins'],
            created_at=datetime.fromisoformat(data['created_at']),
            day_starts_at=data.get('day_starts_at', 0)
        )

    def _deserialize_skill(self, data: Dict):
        from ..models import Skill
        from ..models.skill import CycleType
        return Skill(
            id=data['id'],
            name=data['name'],
            description=data.get('description'),
            color=data.get('color', '#3B82F6'),
            icon_key=data.get('icon_key', '⚡'),
            level=data['level'],
            xp=data['xp'],
            is_archived=data.get('is_archived', False),
            is_focus=data.get('is_focus', False),
            order=data.get('order', 0),
            cycle_type=CycleType(data.get('cycle_type', 'weekly')),
            cycle_start=datetime.fromisoformat(data['cycle_start']) if data.get('cycle_start') else None,
            cycle_end=datetime.fromisoformat(data['cycle_end']) if data.get('cycle_end') else None,
            target_mission_id=data.get('target_mission_id'),
            has_hit_target_this_cycle=data.get('has_hit_target_this_cycle', False),
            missions_count=data.get('missions_count', 0)
        )

    def _deserialize_mission(self, data: Dict):
        from ..models import Mission
        from ..models.mission import ScheduleType
        return Mission(
            id=data['id'],
            title=data['title'],
            note=data.get('note'),
            skill_ids=data.get('skill_ids', []),
            difficulty=data.get('difficulty', 1),
            energy=data.get('energy', 1),
            schedule=ScheduleType(data.get('schedule', 'one_off')),
            due_at=datetime.fromisoformat(data['due_at']) if data.get('due_at') else None,
            is_archived=data.get('is_archived', False),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

    def _deserialize_journal_entry(self, data: Dict):
        from ..models import JournalEntry
        return JournalEntry(
            id=data['id'],
            created_at=datetime.fromisoformat(data['created_at']),
            text=data['text'],
            skill_id=data.get('skill_id'),
            mission_id=data.get('mission_id'),
            is_reflection_token=data.get('is_reflection_token', False),
            edited_at=datetime.fromisoformat(data['edited_at']) if data.get('edited_at') else None
        )

    def _deserialize_capsule(self, data: Dict):
        from ..models import TimeCapsule
        from ..models.capsule import UnlockType
        return TimeCapsule(
            id=data['id'],
            title=data['title'],
            body=data['body'],
            created_at=datetime.fromisoformat(data['created_at']),
            is_encrypted=data.get('is_encrypted', False),
            passphrase_hint=data.get('passphrase_hint'),
            unlock_type=UnlockType(data['unlock_type']),
            unlock_params=data['unlock_params'],
            unlocked_at=datetime.fromisoformat(data['unlocked_at']) if data.get('unlocked_at') else None,
            archived_to_journal_entry_id=data.get('archived_to_journal_entry_id')
        )

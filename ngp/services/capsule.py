"""Time Capsule service - manages capsule creation and unlocking"""

from datetime import datetime
from typing import List, Optional
import uuid
from ..models import TimeCapsule, Player, Skill
from ..models.capsule import UnlockType
from ..services import StorageService


class CapsuleService:
    """
    Manages Time Capsules - letters to your future self.
    Capsules unlock based on various triggers.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def create_capsule(
        self,
        title: str,
        body: str,
        unlock_type: UnlockType,
        unlock_params: dict,
        passphrase: Optional[str] = None,
        passphrase_hint: Optional[str] = None
    ) -> TimeCapsule:
        """
        Create a new time capsule.

        Args:
            title: Capsule title
            body: Letter content
            unlock_type: How to unlock (date/mission/skill_level/player_level)
            unlock_params: Parameters for unlock condition
            passphrase: Optional encryption passphrase
            passphrase_hint: Hint for passphrase

        Returns:
            Created TimeCapsule
        """
        capsule = TimeCapsule(
            id=str(uuid.uuid4()),
            title=title,
            body=body,
            unlock_type=unlock_type,
            unlock_params=unlock_params,
            is_encrypted=passphrase is not None,
            passphrase_hint=passphrase_hint
        )

        # If encrypted, apply simple encryption
        if passphrase:
            capsule.body = self._encrypt(body, passphrase)

        self.storage.save_capsule(capsule)
        return capsule

    def check_and_unlock_capsules(
        self,
        player: Player,
        skills: List[Skill],
        just_completed_mission_id: Optional[str] = None
    ) -> List[TimeCapsule]:
        """
        Check for capsules that should be unlocked.

        Args:
            player: Current player
            skills: Current skills
            just_completed_mission_id: If a mission was just completed

        Returns:
            List of newly unlocked capsules
        """
        locked_capsules = self.storage.get_locked_capsules()
        newly_unlocked = []

        for capsule in locked_capsules:
            if self._should_unlock(capsule, player, skills, just_completed_mission_id):
                capsule.unlock()
                self.storage.save_capsule(capsule)
                newly_unlocked.append(capsule)

        return newly_unlocked

    def _should_unlock(
        self,
        capsule: TimeCapsule,
        player: Player,
        skills: List[Skill],
        just_completed_mission_id: Optional[str]
    ) -> bool:
        """Check if capsule should unlock"""

        if capsule.unlock_type == UnlockType.DATE:
            # Unlock by date
            unlock_date_str = capsule.unlock_params.get('date')
            if unlock_date_str:
                unlock_date = datetime.fromisoformat(unlock_date_str)
                return datetime.now() >= unlock_date

        elif capsule.unlock_type == UnlockType.MISSION_COMPLETION:
            # Unlock when specific mission is completed
            mission_id = capsule.unlock_params.get('mission_id')
            return mission_id == just_completed_mission_id

        elif capsule.unlock_type == UnlockType.SKILL_LEVEL:
            # Unlock when skill reaches level
            skill_id = capsule.unlock_params.get('skill_id')
            required_level = capsule.unlock_params.get('level', 1)

            skill = next((s for s in skills if s.id == skill_id), None)
            if skill:
                return skill.level >= required_level

        elif capsule.unlock_type == UnlockType.PLAYER_LEVEL:
            # Unlock when player reaches level
            required_level = capsule.unlock_params.get('level', 1)
            return player.level >= required_level

        return False

    def decrypt_capsule(self, capsule: TimeCapsule, passphrase: str) -> Optional[str]:
        """
        Decrypt capsule body.

        Args:
            capsule: Capsule to decrypt
            passphrase: Passphrase to try

        Returns:
            Decrypted text or None if wrong passphrase
        """
        if not capsule.is_encrypted:
            return capsule.body

        try:
            return self._decrypt(capsule.body, passphrase)
        except:
            return None

    def archive_to_journal(self, capsule: TimeCapsule) -> str:
        """
        Archive capsule to journal.

        Args:
            capsule: Capsule to archive

        Returns:
            Journal entry ID
        """
        from ..models import JournalEntry

        entry = JournalEntry(
            id=str(uuid.uuid4()),
            text=f"[Time Capsule: {capsule.title}]\n\n{capsule.body}\n\n(Written on {capsule.created_at.strftime('%Y-%m-%d')})",
            created_at=datetime.now()
        )

        self.storage.save_journal_entry(entry)
        capsule.archived_to_journal_entry_id = entry.id
        self.storage.save_capsule(capsule)

        return entry.id

    def _encrypt(self, text: str, passphrase: str) -> str:
        """
        Simple XOR encryption (not cryptographically secure, but fun).
        In production, use proper encryption like Fernet.
        """
        key = passphrase.encode()
        encrypted = bytearray()

        for i, char in enumerate(text.encode()):
            encrypted.append(char ^ key[i % len(key)])

        return encrypted.hex()

    def _decrypt(self, encrypted_hex: str, passphrase: str) -> str:
        """Decrypt XOR-encrypted text"""
        key = passphrase.encode()
        encrypted = bytes.fromhex(encrypted_hex)
        decrypted = bytearray()

        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key[i % len(key)])

        return decrypted.decode()

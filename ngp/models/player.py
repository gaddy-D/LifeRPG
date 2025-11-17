"""Player model - represents the user's character"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Player:
    """
    Represents the player's character in New Game Plus.

    Attributes:
        id: Unique identifier
        display_name: Player's chosen name
        class_name: Player's chosen class/role (e.g., "Digital Craftsman")
        class_description: Optional description of the class
        level: Overall player level
        xp: Current experience points
        coins: In-game currency for rewards
        created_at: When the player was created
        day_starts_at: Hour when the day starts (0-23)
    """
    id: str
    display_name: str
    class_name: str
    level: int = 1
    xp: int = 0
    coins: int = 0
    class_description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    day_starts_at: int = 0  # 0-23, when the day starts for cycle calculations

    def add_xp(self, amount: int) -> bool:
        """
        Add XP to player. Returns True if leveled up.
        """
        self.xp += amount
        xp_needed = self.xp_for_next_level()

        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            return True
        return False

    def xp_for_next_level(self) -> int:
        """Calculate XP needed for next level using curve: ceil(120 × level^1.5)"""
        import math
        return math.ceil(120 * (self.level ** 1.5))

    def add_coins(self, amount: int):
        """Add coins to player"""
        self.coins += amount

    def spend_coins(self, amount: int) -> bool:
        """Spend coins. Returns True if successful, False if insufficient funds"""
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

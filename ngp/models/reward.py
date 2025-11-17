"""Reward model - represents shop items"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Reward:
    """
    Represents a reward in the shop that can be purchased with coins.

    Attributes:
        id: Unique identifier
        title: Reward title
        price_coins: Cost in coins
        note: Optional description
        is_archived: Whether reward is archived
        created_at: When reward was created
        times_redeemed: How many times this has been redeemed
    """
    id: str
    title: str
    price_coins: int
    note: Optional[str] = None
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    times_redeemed: int = 0

    def __post_init__(self):
        """Validate price is positive"""
        if self.price_coins < 0:
            raise ValueError("Price must be non-negative")

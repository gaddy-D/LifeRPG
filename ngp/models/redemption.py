"""Redemption model - tracks reward purchases"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Redemption:
    """
    Records a reward redemption event.

    Attributes:
        id: Unique identifier
        reward_id: ID of redeemed reward
        coins_spent: How many coins were spent
        redeemed_at: When redemption occurred
        note: Optional note about the redemption
    """
    id: str
    reward_id: str
    coins_spent: int
    redeemed_at: datetime = field(default_factory=datetime.now)
    note: str = ""

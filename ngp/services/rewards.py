"""Rewards service - manages the rewards shop"""

import uuid
from typing import List, Optional, Dict
from ..models import Player, Reward, Redemption
from ..services import StorageService


class RewardsService:
    """
    Manages the rewards shop where players can spend coins.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def create_reward(
        self,
        title: str,
        price_coins: int,
        note: Optional[str] = None
    ) -> Reward:
        """
        Create a new reward.

        Args:
            title: Reward title
            price_coins: Cost in coins
            note: Optional description

        Returns:
            Created Reward
        """
        reward = Reward(
            id=str(uuid.uuid4()),
            title=title,
            price_coins=price_coins,
            note=note
        )

        self.storage.save_reward(reward)
        return reward

    def redeem_reward(
        self,
        reward_id: str,
        player: Player,
        note: str = ""
    ) -> Dict[str, any]:
        """
        Redeem a reward if player has enough coins.

        Args:
            reward_id: ID of reward to redeem
            player: Player redeeming
            note: Optional note about redemption

        Returns:
            Dict with redemption info
        """
        reward = self.storage.get_reward(reward_id)
        if not reward:
            raise ValueError(f"Reward {reward_id} not found")

        if reward.is_archived:
            raise ValueError("Cannot redeem archived reward")

        # Check if player has enough coins
        if player.coins < reward.price_coins:
            raise ValueError(
                f"Not enough coins! Need {reward.price_coins}, have {player.coins}"
            )

        # Spend coins
        player.spend_coins(reward.price_coins)
        self.storage.save_player(player)

        # Update reward redemption count
        reward.times_redeemed += 1
        self.storage.save_reward(reward)

        # Record redemption
        redemption = Redemption(
            id=str(uuid.uuid4()),
            reward_id=reward_id,
            coins_spent=reward.price_coins,
            note=note
        )
        self.storage.save_redemption(redemption)

        return {
            'reward': reward,
            'redemption': redemption,
            'coins_remaining': player.coins
        }

    def get_available_rewards(self, player: Player) -> List[Dict[str, any]]:
        """
        Get available rewards with affordability status.

        Args:
            player: Current player

        Returns:
            List of dicts with reward and affordability info
        """
        rewards = self.storage.get_rewards(include_archived=False)
        result = []

        for reward in rewards:
            can_afford = player.coins >= reward.price_coins
            result.append({
                'reward': reward,
                'can_afford': can_afford,
                'coins_needed': max(0, reward.price_coins - player.coins)
            })

        return result

    def archive_reward(self, reward_id: str):
        """Archive a reward"""
        reward = self.storage.get_reward(reward_id)
        if reward:
            reward.is_archived = True
            self.storage.save_reward(reward)

    def get_redemption_history(self, limit: int = 20) -> List[Dict[str, any]]:
        """
        Get recent redemption history with reward details.

        Args:
            limit: Max number of redemptions to return

        Returns:
            List of dicts with redemption and reward info
        """
        redemptions = self.storage.get_redemptions(limit=limit)
        result = []

        for redemption in redemptions:
            reward = self.storage.get_reward(redemption.reward_id)
            result.append({
                'redemption': redemption,
                'reward': reward
            })

        return result

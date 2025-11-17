"""Time and date utilities"""

from datetime import datetime, timedelta
from typing import Tuple


def align_to_day_start(dt: datetime, hour: int = 0) -> datetime:
    """
    Align datetime to the start of the day at specified hour.

    Args:
        dt: Datetime to align
        hour: Hour when day starts (0-23)

    Returns:
        Aligned datetime
    """
    aligned = dt.replace(hour=hour, minute=0, second=0, microsecond=0)

    # If current time is before the day start hour, go to previous day
    if dt.hour < hour:
        aligned -= timedelta(days=1)

    return aligned


def get_cycle_boundaries(
    cycle_type: str,
    reference_time: datetime,
    day_starts_at: int = 0
) -> Tuple[datetime, datetime]:
    """
    Calculate cycle start and end times.

    Args:
        cycle_type: Type of cycle ('daily', 'weekly', 'monthly')
        reference_time: Reference datetime
        day_starts_at: Hour when day starts

    Returns:
        Tuple of (cycle_start, cycle_end)
    """
    aligned = align_to_day_start(reference_time, day_starts_at)

    if cycle_type == 'daily':
        start = aligned
        end = start + timedelta(days=1)

    elif cycle_type == 'weekly':
        # Start of week (Monday)
        days_since_monday = aligned.weekday()
        start = aligned - timedelta(days=days_since_monday)
        end = start + timedelta(weeks=1)

    elif cycle_type == 'monthly':
        # Start of month
        start = aligned.replace(day=1)
        # Start of next month
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)

    else:
        # Default to weekly
        days_since_monday = aligned.weekday()
        start = aligned - timedelta(days=days_since_monday)
        end = start + timedelta(weeks=1)

    return (start, end)


def format_time_remaining(end_time: datetime) -> str:
    """
    Format time remaining until end_time.

    Args:
        end_time: Target datetime

    Returns:
        Human-readable string (e.g., "2d 5h", "3h 20m", "45m")
    """
    now = datetime.now()
    if now >= end_time:
        return "Ended"

    delta = end_time - now

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

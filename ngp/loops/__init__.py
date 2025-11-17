"""
The five core loops of New Game Plus:

1. Action Loop - Complete missions, earn XP
2. Reflection Loop - Journal and reflect on progress
3. Analysis Loop - Navigator analyzes patterns
4. Suggestion Loop - Provide subtle corrective feedback
5. Adjustment Loop - Player refines approach
"""

from .action import ActionLoop
from .reflection import ReflectionLoop
from .analysis import AnalysisLoop
from .suggestion import SuggestionLoop
from .adjustment import AdjustmentLoop

__all__ = [
    'ActionLoop',
    'ReflectionLoop',
    'AnalysisLoop',
    'SuggestionLoop',
    'AdjustmentLoop',
]

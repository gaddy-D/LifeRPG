"""Custom themes for terminal UI"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class ThemeColor(Enum):
    """Theme color roles"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    TEXT = "text"
    TEXT_DIM = "text_dim"
    BACKGROUND = "background"
    ACCENT = "accent"


@dataclass
class Theme:
    """
    Terminal UI theme.

    Attributes:
        name: Theme name
        description: Theme description
        colors: Dict mapping ThemeColor to color code
    """
    name: str
    description: str
    colors: Dict[ThemeColor, str]

    def get_color(self, role: ThemeColor) -> str:
        """Get color for a role"""
        return self.colors.get(role, "#FFFFFF")


# Built-in themes
THEMES = {
    "default": Theme(
        name="Default",
        description="Classic New Game Plus theme",
        colors={
            ThemeColor.PRIMARY: "#3B82F6",        # Blue
            ThemeColor.SECONDARY: "#8B5CF6",      # Purple
            ThemeColor.SUCCESS: "#10B981",        # Green
            ThemeColor.WARNING: "#F59E0B",        # Amber
            ThemeColor.ERROR: "#EF4444",          # Red
            ThemeColor.INFO: "#06B6D4",           # Cyan
            ThemeColor.TEXT: "#F3F4F6",           # Light gray
            ThemeColor.TEXT_DIM: "#9CA3AF",       # Gray
            ThemeColor.BACKGROUND: "#1F2937",     # Dark gray
            ThemeColor.ACCENT: "#4ADE80",         # Light green
        }
    ),

    "cyberpunk": Theme(
        name="Cyberpunk",
        description="Neon cyberpunk aesthetic",
        colors={
            ThemeColor.PRIMARY: "#FF00FF",        # Magenta
            ThemeColor.SECONDARY: "#00FFFF",      # Cyan
            ThemeColor.SUCCESS: "#39FF14",        # Neon green
            ThemeColor.WARNING: "#FFFF00",        # Yellow
            ThemeColor.ERROR: "#FF0040",          # Hot pink
            ThemeColor.INFO: "#00D9FF",           # Electric blue
            ThemeColor.TEXT: "#FFFFFF",           # White
            ThemeColor.TEXT_DIM: "#A0A0A0",       # Gray
            ThemeColor.BACKGROUND: "#0A0A0A",     # Almost black
            ThemeColor.ACCENT: "#FF6EC7",         # Pink
        }
    ),

    "forest": Theme(
        name="Forest",
        description="Calm forest greens",
        colors={
            ThemeColor.PRIMARY: "#10B981",        # Green
            ThemeColor.SECONDARY: "#059669",      # Dark green
            ThemeColor.SUCCESS: "#34D399",        # Light green
            ThemeColor.WARNING: "#FBBF24",        # Amber
            ThemeColor.ERROR: "#F87171",          # Red
            ThemeColor.INFO: "#60A5FA",           # Blue
            ThemeColor.TEXT: "#ECFDF5",           # Very light green
            ThemeColor.TEXT_DIM: "#6EE7B7",       # Medium green
            ThemeColor.BACKGROUND: "#064E3B",     # Dark green
            ThemeColor.ACCENT: "#A7F3D0",         # Mint
        }
    ),

    "ocean": Theme(
        name="Ocean",
        description="Deep ocean blues",
        colors={
            ThemeColor.PRIMARY: "#0EA5E9",        # Sky blue
            ThemeColor.SECONDARY: "#3B82F6",      # Blue
            ThemeColor.SUCCESS: "#06B6D4",        # Cyan
            ThemeColor.WARNING: "#F59E0B",        # Amber
            ThemeColor.ERROR: "#EF4444",          # Red
            ThemeColor.INFO: "#38BDF8",           # Light blue
            ThemeColor.TEXT: "#F0F9FF",           # Very light blue
            ThemeColor.TEXT_DIM: "#7DD3FC",       # Sky blue
            ThemeColor.BACKGROUND: "#082F49",     # Deep blue
            ThemeColor.ACCENT: "#67E8F9",         # Cyan
        }
    ),

    "sunset": Theme(
        name="Sunset",
        description="Warm sunset colors",
        colors={
            ThemeColor.PRIMARY: "#F59E0B",        # Amber
            ThemeColor.SECONDARY: "#EF4444",      # Red
            ThemeColor.SUCCESS: "#10B981",        # Green
            ThemeColor.WARNING: "#FBBF24",        # Yellow
            ThemeColor.ERROR: "#DC2626",          # Dark red
            ThemeColor.INFO: "#F97316",           # Orange
            ThemeColor.TEXT: "#FEF3C7",           # Light yellow
            ThemeColor.TEXT_DIM: "#FCD34D",       # Yellow
            ThemeColor.BACKGROUND: "#7C2D12",     # Dark orange
            ThemeColor.ACCENT: "#FBBF24",         # Amber
        }
    ),

    "monochrome": Theme(
        name="Monochrome",
        description="Classic black and white",
        colors={
            ThemeColor.PRIMARY: "#FFFFFF",        # White
            ThemeColor.SECONDARY: "#D1D5DB",      # Light gray
            ThemeColor.SUCCESS: "#9CA3AF",        # Gray
            ThemeColor.WARNING: "#6B7280",        # Medium gray
            ThemeColor.ERROR: "#374151",          # Dark gray
            ThemeColor.INFO: "#E5E7EB",           # Very light gray
            ThemeColor.TEXT: "#F9FAFB",           # Almost white
            ThemeColor.TEXT_DIM: "#9CA3AF",       # Gray
            ThemeColor.BACKGROUND: "#111827",     # Almost black
            ThemeColor.ACCENT: "#FFFFFF",         # White
        }
    ),

    "dracula": Theme(
        name="Dracula",
        description="Popular Dracula color scheme",
        colors={
            ThemeColor.PRIMARY: "#BD93F9",        # Purple
            ThemeColor.SECONDARY: "#FF79C6",      # Pink
            ThemeColor.SUCCESS: "#50FA7B",        # Green
            ThemeColor.WARNING: "#F1FA8C",        # Yellow
            ThemeColor.ERROR: "#FF5555",          # Red
            ThemeColor.INFO: "#8BE9FD",           # Cyan
            ThemeColor.TEXT: "#F8F8F2",           # Foreground
            ThemeColor.TEXT_DIM: "#6272A4",       # Comment
            ThemeColor.BACKGROUND: "#282A36",     # Background
            ThemeColor.ACCENT: "#FFB86C",         # Orange
        }
    ),
}


class ThemeManager:
    """Manages themes"""

    def __init__(self):
        self.current_theme = THEMES["default"]
        self.custom_themes: Dict[str, Theme] = {}

    def set_theme(self, theme_name: str):
        """Set active theme"""
        if theme_name in THEMES:
            self.current_theme = THEMES[theme_name]
        elif theme_name in self.custom_themes:
            self.current_theme = self.custom_themes[theme_name]
        else:
            raise ValueError(f"Theme {theme_name} not found")

    def add_custom_theme(self, theme: Theme):
        """Add a custom theme"""
        self.custom_themes[theme.name.lower()] = theme

    def get_color(self, role: ThemeColor) -> str:
        """Get color for current theme"""
        return self.current_theme.get_color(role)

    def list_themes(self) -> List[str]:
        """List all available themes"""
        return list(THEMES.keys()) + list(self.custom_themes.keys())

    def get_theme(self, theme_name: str) -> Theme:
        """Get a theme by name"""
        if theme_name in THEMES:
            return THEMES[theme_name]
        return self.custom_themes.get(theme_name, THEMES["default"])

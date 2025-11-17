"""Plugin system for extensibility"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import importlib.util
import sys
from pathlib import Path


class PluginType(Enum):
    """Plugin types"""
    MISSION_GENERATOR = "mission_generator"
    ANALYSIS_HOOK = "analysis_hook"
    EXPORT_FORMATTER = "export_formatter"
    UI_THEME = "ui_theme"
    CUSTOM_METRIC = "custom_metric"


@dataclass
class Plugin:
    """
    Represents a plugin.

    Attributes:
        id: Unique plugin ID
        name: Plugin name
        version: Plugin version
        plugin_type: Type of plugin
        description: Plugin description
        author: Plugin author
        enabled: Whether plugin is enabled
        handler: The plugin's handler function
    """
    id: str
    name: str
    version: str
    plugin_type: PluginType
    description: str
    author: str = "Unknown"
    enabled: bool = True
    handler: Optional[Callable] = None


class PluginManager:
    """
    Manages plugins and extensibility.
    """

    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}

    def register_plugin(self, plugin: Plugin):
        """
        Register a plugin.

        Args:
            plugin: Plugin to register
        """
        self.plugins[plugin.id] = plugin

        # Register hooks based on plugin type
        if plugin.plugin_type == PluginType.ANALYSIS_HOOK:
            self.register_hook("on_analysis", plugin.handler)
        elif plugin.plugin_type == PluginType.MISSION_GENERATOR:
            self.register_hook("generate_mission", plugin.handler)
        elif plugin.plugin_type == PluginType.EXPORT_FORMATTER:
            self.register_hook("format_export", plugin.handler)

    def register_hook(self, hook_name: str, callback: Callable):
        """
        Register a hook callback.

        Args:
            hook_name: Name of the hook
            callback: Callback function
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []

        self.hooks[hook_name].append(callback)

    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Trigger all callbacks for a hook.

        Args:
            hook_name: Name of the hook
            *args: Positional arguments for callbacks
            **kwargs: Keyword arguments for callbacks

        Returns:
            List of results from all callbacks
        """
        if hook_name not in self.hooks:
            return []

        results = []
        for callback in self.hooks[hook_name]:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Plugin error in {hook_name}: {e}")

        return results

    def load_plugin_from_file(self, filepath: str) -> Optional[Plugin]:
        """
        Load a plugin from a Python file.

        Args:
            filepath: Path to plugin file

        Returns:
            Loaded Plugin object or None
        """
        try:
            spec = importlib.util.spec_from_file_location("plugin", filepath)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules["plugin"] = module
            spec.loader.exec_module(module)

            # Plugin file should define PLUGIN constant
            if hasattr(module, 'PLUGIN'):
                plugin = module.PLUGIN
                self.register_plugin(plugin)
                return plugin

        except Exception as e:
            print(f"Failed to load plugin from {filepath}: {e}")

        return None

    def load_plugins_from_directory(self, directory: str):
        """
        Load all plugins from a directory.

        Args:
            directory: Directory containing plugin files
        """
        plugin_dir = Path(directory)
        if not plugin_dir.exists():
            return

        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            self.load_plugin_from_file(str(plugin_file))

    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get a plugin by ID"""
        return self.plugins.get(plugin_id)

    def list_plugins(self, plugin_type: Optional[PluginType] = None) -> List[Plugin]:
        """
        List all plugins, optionally filtered by type.

        Args:
            plugin_type: Optional filter by type

        Returns:
            List of plugins
        """
        if plugin_type:
            return [p for p in self.plugins.values() if p.plugin_type == plugin_type]
        return list(self.plugins.values())

    def enable_plugin(self, plugin_id: str):
        """Enable a plugin"""
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = True

    def disable_plugin(self, plugin_id: str):
        """Disable a plugin"""
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = False


# Example plugin for demonstration
EXAMPLE_ANALYSIS_PLUGIN = Plugin(
    id="example_motivational_boost",
    name="Motivational Boost",
    version="1.0.0",
    plugin_type=PluginType.ANALYSIS_HOOK,
    description="Adds motivational messages to analysis",
    author="New Game Plus Team",
    handler=lambda patterns: patterns + ["You're doing great! Keep it up! 🚀"]
)

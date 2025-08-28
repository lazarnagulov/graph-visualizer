import os
import sys
from typing import Tuple, List, Dict, Optional

from jinja2 import Template
from visualizer.api.service.plugin import Plugin
from visualizer.core.service.plugin_service import VISUALIZER_PLUGIN, DATA_SOURCE_PLUGIN
from visualizer.core.usecase.plugin_manager import PluginManager


def render(
    plugin_manager: PluginManager,
    workspaces: Optional[List[Dict[str, str]]] = None,
    selected_workspace: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Returns header and body HTML content including workspace info.
    """
    # Load the template file for the app header
    with open(os.path.join(sys.prefix, 'templates/app_header_template.html'), 'r', encoding='utf-8') as file:
        body_template = file.read()

    # Get lists of available plugins from the plugin service
    visualizer_plugins: List[Plugin] = plugin_manager.plugin_service.plugins[VISUALIZER_PLUGIN]
    data_source_plugins: List[Plugin] = plugin_manager.plugin_service.plugins[DATA_SOURCE_PLUGIN]

    # Convert plugins into dicts suitable for Jinja template rendering
    visualizer_plugins_js: List[Dict[str, str]] = [
        {"name": plugin.name(), "id": plugin.identifier()}
        for plugin in visualizer_plugins
    ]
    data_source_plugins_js: List[Dict[str, str]] = [
        {"name": plugin.name(), "id": plugin.identifier()}
        for plugin in data_source_plugins
    ]

    # Safe access to avoid AttributeError if plugin is None
    selected_visualizer = plugin_manager.visualizer_plugin.identifier() if plugin_manager.visualizer_plugin else ""
    selected_data_source = plugin_manager.data_source_plugin.identifier() if plugin_manager.data_source_plugin else ""

    # --- Workspace counter logic ---
    total_workspaces = len(workspaces or [])
    current_workspace_index = 0
    if selected_workspace and total_workspaces > 0:
        for i, ws in enumerate(workspaces):
            if ws.get("id") == selected_workspace:
                current_workspace_index = i + 1  # 1-based index
                break

    # Render the template with all necessary variables for the header
    body_html = Template(body_template).render(
        visualizer_plugins=visualizer_plugins_js,
        data_source_plugins=data_source_plugins_js,
        selected_visualizer=selected_visualizer,
        selected_data_source=selected_data_source,
        workspaces=workspaces or [],
        selected_workspace=selected_workspace,
        total_workspaces=total_workspaces,
        current_workspace_index=current_workspace_index
    )

    # Return empty string for head (no JS needed) and the rendered body
    return "", body_html

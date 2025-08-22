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
    with open(os.path.join(sys.prefix, 'templates/app_header_template.html'), 'r', encoding='utf-8') as file:
        body_template = file.read()

    visualizer_plugins: List[Plugin] = plugin_manager.plugin_service.plugins[VISUALIZER_PLUGIN]
    data_source_plugins: List[Plugin] = plugin_manager.plugin_service.plugins[DATA_SOURCE_PLUGIN]

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

    body_html = Template(body_template).render(
        visualizer_plugins=visualizer_plugins_js,
        data_source_plugins=data_source_plugins_js,
        selected_visualizer=selected_visualizer,
        selected_data_source=selected_data_source,
        workspaces=workspaces or [],
        selected_workspace=selected_workspace,
    )

    return "", body_html

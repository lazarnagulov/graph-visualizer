import os
import sys
from typing import Tuple, List, Dict

from jinja2 import Template
from visualizer.api.service.plugin import Plugin
from visualizer.core.service.plugin_service import VISUALIZER_PLUGIN, DATA_SOURCE_PLUGIN
from visualizer.core.usecase.plugin_manager import PluginManager


def render(plugin_manager: PluginManager) -> Tuple[str, str]:
    """
    Returns the required header and body html content that needs to be included in page
    in order to display the app header.

    :return: (header,body) html string that should be included in page.
    """

    with open(os.path.join(sys.prefix, 'templates/app_header_template.html'), 'r', encoding='utf-8') as file:
        body_template = file.read()

    visualizer_plugins: List[Plugin] = plugin_manager.plugin_service.plugins[VISUALIZER_PLUGIN]
    data_source_plugins: List[Plugin]  = plugin_manager.plugin_service.plugins[DATA_SOURCE_PLUGIN]

    visualizer_plugins_js: List[Dict[str ,str]] = [
        {"name": plugin.name(), "id": plugin.identifier()}
        for plugin in visualizer_plugins]
    data_source_plugins_js: List[Dict[str ,str]]  = [
        {"name": plugin.name(), "id": plugin.identifier()}
        for plugin in data_source_plugins]

    body_html = Template(body_template).render(visualizer_plugins=visualizer_plugins_js,
                                               data_source_plugins=data_source_plugins_js,
                                               selected_visualizer=plugin_manager.visualizer_plugin.identifier(),
                                               selected_data_source=plugin_manager.data_source_plugin.identifier())
    return "", body_html
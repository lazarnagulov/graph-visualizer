from django.apps import AppConfig
from visualizer.core.platform.platform import Platform
from visualizer.core.service.plugin_service import PluginService

datasource_group = 'visualizer.datasource'
visualizer_group = "visualizer.visualizer"

class GraphExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer'
    plugin_service = PluginService()
    platform = Platform(plugin_service)

    def ready(self):
        self.plugin_service.load_plugins(datasource_group)
        self.plugin_service.load_plugins(visualizer_group)
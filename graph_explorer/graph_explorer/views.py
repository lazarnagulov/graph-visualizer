from django.apps import apps
from django.shortcuts import render, redirect
from visualizer.core.service.plugin_service import PluginService

from .apps import datasource_group, visualizer_group


def index(request):
    plugin_service: PluginService = apps.get_app_config('graph_explorer').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]
    return render(request, 'index.html', {
        'title': 'Index',
        'datasource_plugins': datasource_plugins,
        'visualizer_plugins': visualizer_plugins
    })

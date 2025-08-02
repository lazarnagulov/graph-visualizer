from django.apps import apps
from django.shortcuts import render, redirect
from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService

from visualizer.core.platform.platform import Platform
from visualizer.core.view import main_view
from visualizer.core.view.main_view import MainView

from .apps import datasource_group, visualizer_group

from pprint import pprint


def plugins(request):
    plugin_service: PluginService = apps.get_app_config('graph_explorer').plugin_service
    datasource_plugins = plugin_service.plugins[datasource_group]
    visualizer_plugins = plugin_service.plugins[visualizer_group]
    return render(request, 'plugins.html', {
        'title': 'Plugins',
        'datasource_plugins': datasource_plugins,
        'visualizer_plugins': visualizer_plugins
    })

def index(request):
    plugin_service: PluginService = apps.get_app_config('graph_explorer').plugin_service
    platform: Platform = apps.get_app_config('graph_explorer').platform
    workspace: Workspace = platform.get_selected_workspace()
    workspace.visualizer_plugin = plugin_service.plugins[visualizer_group][0]
    workspace.data_source_plugin = plugin_service.plugins[datasource_group][0]
    main_view: MainView = workspace.generate_main_view()
    _,main_view_html = main_view.render()
    _,app_header = workspace.render_app_header()

    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'app_header': app_header,
        'main_view': main_view_html,
    })
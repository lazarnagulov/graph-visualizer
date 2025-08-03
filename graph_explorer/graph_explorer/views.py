from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService

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
    workspace: Workspace = __get_workspace()
    _,main_view_html = workspace.render_main_view()
    _,app_header = workspace.render_app_header()

    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'app_header': app_header,
        'main_view': main_view_html,
    })


def visualizer_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    workspace: Workspace = __get_workspace()
    __get_workspace().set_visualizer_plugin(plugin_id)
    _,main_view_html = workspace.render_main_view()
    return HttpResponse(main_view_html)

def data_source_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    workspace: Workspace = __get_workspace()
    __get_workspace().set_data_source_plugin(plugin_id)
    _,main_view_html = workspace.render_main_view()
    return HttpResponse(main_view_html)

def data_file_upload(request):
    workspace: Workspace = __get_workspace()
    if request.method == "POST" and 'file_input' in request.FILES:
        uploaded_file:UploadedFile = request.FILES['file_input']
        file_string = uploaded_file.read()
        workspace.data_file_string = file_string
        workspace.generate_graph()

    _,main_view_html = workspace.render_main_view()
    return HttpResponse(main_view_html)

def __get_workspace() -> Workspace:
    return apps.get_app_config('graph_explorer').platform.get_selected_workspace()
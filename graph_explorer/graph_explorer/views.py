from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from visualizer.core.command.command_result import CommandResult, CommandStatus
from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService

from .apps import datasource_group, visualizer_group


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
    workspace: Workspace = __get_workspace()
    main_view_head, plugin_head, main_view_body = workspace.render_main_view()
    _,app_header = workspace.render_app_header()

    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'app_header': app_header,
        'main_view': main_view_body,
        'head': main_view_head + plugin_head,
    })


def visualizer_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    workspace: Workspace = __get_workspace()
    workspace.set_visualizer_plugin(plugin_id)
    _,plugin_head,main_view_body = workspace.render_main_view()
    return HttpResponse(plugin_head + main_view_body)

def data_source_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    __get_workspace().set_data_source_plugin(plugin_id)
    return generate_graph(request) # we will not update the head since the visualizer hasn't changed

def data_file_upload(request):
    workspace: Workspace = __get_workspace()
    if request.method == "POST" and 'file_input' in request.FILES:
        uploaded_file:UploadedFile = request.FILES['file_input']
        file_string = uploaded_file.read()
        workspace.data_file_string = file_string
        workspace.generate_graph()

    _,_,main_view_body = workspace.render_main_view()
    return HttpResponse(main_view_body) # we will not update the head since the visualizer hasn't changed

def execute_command(request):
    command: str = request.POST.get('command').strip()
    if not command:
        return __build_cli_response("No input provided. Please enter a command.", CommandStatus.ERROR)

    workspace: Workspace = __get_workspace()
    result: CommandResult = workspace.execute_command(command)

    trigger = "graph-updated" if result.status == CommandStatus.OK else None
    return __build_cli_response(result.output, result.status, trigger)

def generate_graph(_request):
    workspace: Workspace = __get_workspace()
    _,_, main_view_html = workspace.render_main_view()
    return HttpResponse(main_view_html)

def filter_graph(request):
    workspace: Workspace = __get_workspace()
    error = workspace.filter_graph(
        request.POST.get('key'),
        request.POST.get('operator'),
        request.POST.get('value')
    )
    if error:
        response = HttpResponse(error)
        response["HX-Reswap"] = "innerHTML"
        response["HX-Retarget"] = "#filter-error"
        return response
    else:
        _,_, main_view_html = workspace.render_main_view()
        return HttpResponse(main_view_html)

def search_graph(request):
    workspace: Workspace = __get_workspace()
    workspace.search_graph(request.POST.get('query'))
    return generate_graph(request)

def reload_graph(request):
    workspace: Workspace = __get_workspace()
    workspace.generate_graph()
    return generate_graph(request)

def __get_workspace() -> Workspace:
    return apps.get_app_config('graph_explorer').platform.get_selected_workspace()

def __build_cli_response(output: str, status: CommandStatus, trigger: str = None) -> HttpResponse:
    response = HttpResponse(render_to_string('cli_output.html', {
        "output": output,
        "status": status.value,
    }))
    if trigger:
        response["HX-Trigger"] = trigger
    response["HX-Reswap"] = "innerHTML"
    response["HX-Retarget"] = "#terminal-output"
    return response
from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from visualizer.core.command.command_result import CommandResult, CommandStatus
from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService
from visualizer.core.platform.platform import Platform

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
    tree_view_head, tree_view_body = workspace.render_tree_view()
    platform = apps.get_app_config('graph_explorer').platform
    workspaces_list = [{"id": ws.id} for ws in platform.list_workspaces()]
    _, app_header = workspace.render_app_header(workspaces=workspaces_list, selected_workspace=platform.current_workspace_id)
    bird_view_head, bird_view_body = workspace.render_bird_view()

    return render(request, 'index.html', {
        'title': 'Graph Explorer',
        'app_header': app_header,
        'main_view': main_view_body,
        'head': main_view_head + plugin_head + tree_view_head + bird_view_head,
        'tree_view': tree_view_body,
        'bird_view': bird_view_body
    })


def visualizer_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    workspace: Workspace = __get_workspace()
    workspace.set_visualizer_plugin(plugin_id)
    return __build_views_response(workspace, True)


def data_source_change(request):
    plugin_id: str = request.GET.get('plugin_id')
    workspace: Workspace = __get_workspace()
    try:
        workspace.set_data_source_plugin(plugin_id)
    except Exception as e:
        response = HttpResponse(str(e), content_type="text/plain")
        response["HX-Reswap"] = "innerHTML"
        response["HX-Retarget"] = "#loader-error"
        return response

    return __build_views_response(workspace)


def data_file_upload(request):
    workspace: Workspace = __get_workspace()
    if request.method == "POST" and 'file_input' in request.FILES:
        uploaded_file: UploadedFile = request.FILES['file_input']
        file_string = uploaded_file.read()
        keys = request.POST.getlist("extra_keys")
        values = request.POST.getlist("extra_values")
        extra_props = {k: v for k, v in zip(keys, values) if k.strip()}
        workspace.data_file_string = file_string
        try:
            workspace.generate_graph(**extra_props)
        except Exception as e:
            response = HttpResponse(str(e), content_type="text/plain")
            response["HX-Reswap"] = "innerHTML"
            response["HX-Retarget"] = "#loader-error"
            return response

    return __build_views_response(workspace)


def execute_command(request):
    command: str = request.POST.get('command').strip()
    if not command:
        return __build_cli_response("No input provided. Please enter a command.", CommandStatus.ERROR)

    workspace: Workspace = __get_workspace()
    result: CommandResult = workspace.execute_command(command)

    trigger = "graph-updated" if result.status == CommandStatus.OK else None
    return __build_cli_response(result.output, result.status, trigger)


def generate_graph(_request):
    return __build_views_response()


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
        return __build_views_response(workspace)


def search_graph(request):
    workspace: Workspace = __get_workspace()
    workspace.search_graph(request.POST.get('query'))
    return __build_views_response(workspace)


def reload_graph(_request):
    workspace: Workspace = __get_workspace()
    workspace.generate_graph(True)
    return __build_views_response(workspace)


def create_workspace(_request):
    platform = apps.get_app_config('graph_explorer').platform
    platform.create_workspace()
    return __build_workspace_response(platform)


def delete_workspace(_request):
    platform = apps.get_app_config('graph_explorer').platform
    current_id = platform.current_workspace_id
    platform.delete_workspace(current_id)
    return __build_workspace_response(platform)


def switch_workspace_next(_request):
    platform = apps.get_app_config('graph_explorer').platform
    platform.switch_to_next_workspace()
    return __build_workspace_response(platform)


def switch_workspace_back(_request):
    platform = apps.get_app_config('graph_explorer').platform
    platform.switch_to_previous_workspace()
    return __build_workspace_response(platform)


def __build_workspace_response(platform: Platform):
    workspace = platform.get_selected_workspace()

    workspaces_list = [{"id": ws.id} for ws in platform.list_workspaces()]
    _, app_header = workspace.render_app_header(workspaces=workspaces_list,
                                                selected_workspace=platform.current_workspace_id)

    main_view_head, plugin_head, main_view_body = workspace.render_main_view()
    tree_view_head, tree_view_body = workspace.render_tree_view()

    body = main_view_body + tree_view_body

    return HttpResponse(app_header + body)


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


def __build_views_response(workspace: Workspace = None, include_plugin_head=False, include_all_heads=False) -> HttpResponse:
    if not workspace:
        workspace: Workspace = __get_workspace()
    main_view_head, plugin_head, main_view_body = workspace.render_main_view()
    tree_view_head, tree_view_body = workspace.render_tree_view()
    if include_all_heads:
        head = main_view_head + plugin_head + tree_view_head
    elif include_plugin_head:
        head = plugin_head
    else:
        head = ""
    body = main_view_body + tree_view_body

    return HttpResponse(head + body)

from typing import List

from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService


class Platform:
    def __init__(self, plugin_service: PluginService):
        self.plugin_service = plugin_service
        self.workspaces: dict[str, Workspace] = {}
        self.current_workspace_id: str = None
        self.create_workspace()  # create a default workspace

    def create_workspace(self) -> Workspace:
        """Create a new workspace and set it as the current workspace."""
        ws = Workspace(self.plugin_service)
        self.workspaces[ws.id] = ws
        self.current_workspace_id = ws.id
        return ws
    

    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete an existing workspace. Automatically switch to the next workspace if possible."""
        if workspace_id not in self.workspaces:
            return False

        # Get ordered list of workspace IDs
        ids = list(self.workspaces.keys())
        idx = ids.index(workspace_id)  # index of workspace to delete

        # Delete the workspace
        del self.workspaces[workspace_id]

        # Determine new current_workspace_id
        remaining_ids = list(self.workspaces.keys())
        if remaining_ids:
            if idx < len(remaining_ids):
                self.current_workspace_id = remaining_ids[idx]  # next workspace
            else:
                self.current_workspace_id = remaining_ids[-1]  # last workspace if deleted was last
        else:
            self.current_workspace_id = None  # no workspace left

        # Regenerate graph if needed
        if self.current_workspace_id:
            current_ws = self.workspaces[self.current_workspace_id]
            if current_ws.data_file_string:
                current_ws.generate_graph()

        return True



    def get_selected_workspace(self) -> Workspace:
        """Return the currently selected workspace."""
        if self.current_workspace_id:
            return self.workspaces[self.current_workspace_id]
        return self.create_workspace()

    def switch_workspace(self, workspace_id: str) -> bool:
        """
        Switch the current workspace to the specified one and refresh its context.
        
        Automatically regenerates the graph if the workspace already has data loaded.
        """
        if workspace_id in self.workspaces:
            self.current_workspace_id = workspace_id
            workspace = self.workspaces[workspace_id]
            # Automatically regenerate the graph when switching
            if workspace.data_file_string:  # Only if there is data to generate from
                workspace.generate_graph()
            return True
        return False

    def list_workspaces(self) -> List[Workspace]:
        """Return a list of all workspaces."""
        return list(self.workspaces.values())
    
    

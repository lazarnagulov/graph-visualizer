from typing import List, Callable, Dict, Any

from visualizer.api.model.graph import Graph
from visualizer.core.cli.command_parser import parse_command
from visualizer.core.command import Command
from visualizer.core.command.command_result import CommandResult, CommandStatus


class CommandHistoryEmptyError(Exception): 
    """Raised when undo or redo operation cannot be performed because history is empty."""
    ...

class CommandService:

    __slots__ = ["__undo_stack", "__redo_stack", "__graph_generator"]

    def __init__(self, graph_generator: Callable[..., None]) -> None:
        """
        Initialize the CommandService with undo and redo stacks.

        This sets up internal stacks to manage command history, allowing support for undoing
        and redoing commands.
        """
        self.__graph_generator: Callable[..., None] = graph_generator
        self.__undo_stack: List[Command] = []
        self.__redo_stack: List[Command] = []

    def execute_command(self, graph: Graph, command_input: str, **kwargs) -> CommandResult:
        """
        Parse and execute a command string.

        :param graph: The graph object on which the command will be executed.
        :param command_input: The command string to parse and execute.
        :return: A `CommandResult` indicating the outcome.
        """
        try:
            match command_input:
                case "undo":
                    self.undo()
                    return CommandResult(CommandStatus.OK, "Undo successful")

                case "redo":
                    self.redo()
                    return CommandResult(CommandStatus.OK, "Redo successful")

                case "help":
                    return CommandResult(CommandStatus.INFO, self.help())

                case "reload":
                    self.__graph_generator(**kwargs)
                    return CommandResult.success()

                case _:
                    command: Command = parse_command(graph, command_input)
                    self.execute(command)
                    return CommandResult.success()

        except Exception as e:
            return CommandResult(CommandStatus.ERROR, str(e))

    def execute(self, command: Command) -> None:
        """
        Execute a command and push it onto the undo stack.

        This method performs the command's action by calling `execute()`, then adds it
        to the undo stack and clears the redo stack.

        :param command: The command to execute.
        :type command: Command
        """
        command.execute()
        self.__undo_stack.append(command)
        self.__redo_stack.clear()

    def undo(self) -> None:
        """
        Undo the most recently executed command.

        If the undo stack is not empty, the last command is undone and pushed onto
        the redo stack.
        """
        if self.__undo_stack:
            command: Command = self.__undo_stack.pop()
            command.undo()
            self.__redo_stack.append(command)
        else:
            raise CommandHistoryEmptyError("Nothing to undo.")

    def redo(self) -> None:
        """
        Redo the most recently undone command.

        If the redo stack is not empty, the last undone command is re-executed
        and pushed back onto the undo stack.
        """
        if self.__redo_stack:
            command: Command = self.__redo_stack.pop()
            command.execute()
            self.__undo_stack.append(command)
        else:
            raise CommandHistoryEmptyError("Nothing to redo.")

    def help(self) -> str:
        """ Return the help text. """
        return "Possible commands are create, edit, delete, filter, search, reload, undo, redo and help."
from typing import List

from visualizer.core.command import Command


class CommandHistoryEmptyError(Exception): 
    """Raised when undo or redo operation cannot be performed because history is empty."""
    ...

class CommandService:

    __slots__ = ["__undo_stack", "__redo_stack"]

    def __init__(self) -> None:
        """
        Initialize the CommandService with undo and redo stacks.

        This sets up internal stacks to manage command history, allowing support for undoing
        and redoing commands.
        """
        self.__undo_stack: List[Command] = []
        self.__redo_stack: List[Command] = []

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
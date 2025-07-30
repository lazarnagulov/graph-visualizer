from typing import List

from visualizer.core.usecase.command.command import Command


class CommandService:

    __slots__ = ["__undo_stack", "__redo_stack"]

    def __init__(self) -> None:
        self.__undo_stack: List[Command] = []
        self.__redo_stack: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.__undo_stack.append(command)
        self.__redo_stack.clear()

    def undo(self) -> None:
        if self.__undo_stack:
            command: Command = self.__undo_stack.pop()
            command.undo()
            self.__redo_stack.append(command)

    def redo(self) -> None:
        if self.__redo_stack:
            command: Command = self.__redo_stack.pop()
            command.execute()
            self.__undo_stack.append(command)
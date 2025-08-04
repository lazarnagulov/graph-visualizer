from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for command pattern.

    This class defines the interface for commands that support execution and undoing.
    Subclasses must implement both the `execute` and `undo` methods.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command.

        This method should be implemented by subclasses to define the specific
        action that the command performs.
        """
        ...

    @abstractmethod
    def undo(self) -> None:
        """
        Undo the command.

        This method should be implemented by subclasses to define how to revert
        the action performed by `execute`.
        """
        ...
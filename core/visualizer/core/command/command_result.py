from dataclasses import dataclass
from enum import Enum


class CommandStatus(str, Enum):
    """
    Enum representing the possible statuses of a command execution.

    Attributes:
        OK: Indicates the command completed successfully.
        ERROR: Indicates the command encountered an error.
    """
    OK = "ok"
    ERROR = "error"


@dataclass
class CommandResult:
    """
    Represents the result of executing a command.

    This data class holds the status and output message resulting from a command's execution.

    :param status: A status of the command (OK, ERROR).
    :type status: CommandStatus
    :param output: A string containing the output or message from the command execution.
    :type output: str
    """
    status: CommandStatus
    output: str
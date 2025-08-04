from dataclasses import dataclass


@dataclass
class CommandResult:
    """
    Represents the result of executing a command.

    This data class holds the status and output message resulting from a command's execution.

    :param status: A string indicating the status of the command (e.g., "success", "error").
    :type status: str
    :param output: A string containing the output or message from the command execution.
    :type output: str
    """
    status: str
    output: str
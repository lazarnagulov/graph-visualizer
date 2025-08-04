from dataclasses import dataclass


@dataclass
class CommandResult:
    status: str
    output: str
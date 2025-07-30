

class ParserError(Exception):
    """Exception raised when trying to remove a node that has edges attached."""
    def __init__(self, message: str):
        super().__init__(message)

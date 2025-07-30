

class ParserError(Exception):
    """Exception raised when parser error occurs."""
    def __init__(self, message: str):
        super().__init__(message)

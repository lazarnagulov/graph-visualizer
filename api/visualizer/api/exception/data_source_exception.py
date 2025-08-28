class MissingRequiredParameterError(Exception):
    """
    Exception raised when a required parameter is missing from input.

    This is used in plugin where specific parameters must be provided for successful execution.
    """
    ...


class InvalidParameterValueError(Exception):
    """
    Exception raised when a provided parameter has an invalid or unsupported value.

    This may occur during plugin execution or data loading when input
    (e.g., file content, API key, configuration) is present but does not meet
    the expected format, structure, or validity.

    Examples:
        - File content is not valid JSON
        - API key is in the wrong format or unauthorized
        - Input data doesn't match the required schema
    """
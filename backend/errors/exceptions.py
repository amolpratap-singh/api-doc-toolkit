class ToolkitError(Exception):
    """Base class for all exceptions in the toolkit."""
    pass

class SpecParseError(ToolkitError):
    """Raised when there is an error parsing the specification."""
    pass

class InvalidDirectoryError(ToolkitError):
    """Raised when a specified directory path is invalid."""
    pass

class ExecutionError(ToolkitError):
    """Raised when there is an error during API execution."""
    pass
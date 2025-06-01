class FileUtilityError(Exception):
    """Base exception for file utility errors"""
    pass

class InvalidDirectoryError(FileUtilityError):
    """Raised when an invalid directory is provided"""
    pass

class NoSpecFilesFoundError(FileUtilityError):
    """Raised when no specification files are found"""
    pass

class UnsupportedFileTypeError(FileUtilityError):
    """Raised when an unsupported file type is encountered"""
    pass
import os
import logging

from pathlib import Path
from typing import List, Dict
from errors.exception import (InvalidDirectoryError, NoSpecFilesFoundError, UnsupportedFileTypeError)

class APISpecFileUtility:
    """
    Utility class for handling API specification files in a directory.
    Supports JSON, YAML, and YML files for API specifications.
    """
    
    VALID_EXTENSIONS = {'.json', '.yaml', '.yml'}
    
    def __init__(self, directory_path: str):
        """
        Initialize the file utility with a directory path.
        
        Args:
            directory_path: Path to the directory containing API spec files
            
        Raises:
            InvalidDirectoryError: If the directory doesn't exist or isn't accessible
        """
        logger = logging.getLogger("APISpecFileUtility")
        logger.info(f"Initializing APISpecFileUtility with directory: {directory_path}")
        
        self.directory_path = directory_path
        self._validate_directory()
        
    def _validate_directory(self) -> None:
        if not os.path.exists(self.directory_path):
            raise InvalidDirectoryError(f"Directory does not exist: {self.directory_path}")
        if not os.path.isdir(self.directory_path):
            raise InvalidDirectoryError(f"Path is not a directory: {self.directory_path}")
        if not os.access(self.directory_path, os.R_OK):
            raise InvalidDirectoryError(f"Directory not readable: {self.directory_path}")
    
    def get_spec_files(self) -> List[Path]:
        """
        Get all API specification files in the directory.
        
        Returns:
            List of Path objects for each spec file found
            
        Raises:
            NoSpecFilesFoundError: If no spec files are found
        """
        spec_files = []
        
        for item in os.listdir(self.directory_path):
            file_path = Path(self.directory_path) / item
            if file_path.is_file() and file_path.suffix.lower() in self.VALID_EXTENSIONS:
                spec_files.append(file_path)
                
        if not spec_files:
            raise NoSpecFilesFoundError(
                f"No API spec files found in {self.directory_path}. "
                f"Supported extensions: {', '.join(self.VALID_EXTENSIONS)}"
            )
            
        return spec_files
    
    def get_file_contents(self, file_path: Path) -> str:
        """
        Read the contents of a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Contents of the file as a string
            
        Raises:
            UnsupportedFileTypeError: If file extension is not supported
            IOError: If file cannot be read
        """
        if file_path.suffix.lower() not in self.VALID_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {file_path.suffix}. "
                f"Supported types: {', '.join(self.VALID_EXTENSIONS)}"
            )
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def group_files_by_extension(self) -> Dict[str, List[Path]]:
        """
        Group found specification files by their extension.
        
        Returns:
            Dictionary mapping extensions to lists of files
        """
        spec_files = self.get_spec_files()
        grouped = {ext: [] for ext in self.VALID_EXTENSIONS}
        
        for file in spec_files:
            grouped[file.suffix.lower()].append(file)
            
        return grouped
    
    def has_multiple_spec_files(self) -> bool:
        """
        Check if there are multiple specification files in the directory.
        
        Returns:
            True if multiple files exist, False if single or none
        """
        try:
            return len(self.get_spec_files()) > 1
        except NoSpecFilesFoundError:
            return False
    
    @staticmethod
    def is_valid_spec_file(file_path: str) -> bool:
        """
        Check if a file is a valid API specification file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if valid, False otherwise
        """
        path = Path(file_path)
        return path.is_file() and path.suffix.lower() in APISpecFileUtility.VALID_EXTENSIONS
#!/usr/bin/env python3
import os
import yaml
import json
import traceback

class APISpecMerger:
    """
    Merges multiple or single API specification files into a single YAML file.
    This class reads all YAML files in a specified directory, merges their paths and component schemas,
    and writes the final merged specification to an output file.
    Attributes:
        spec_file_dir (str): Directory containing the API specification files.
        out_spec_file (str): Output file path for the merged API specification.
    """
    def __init__(self, spec_file_dir, out_spec_file):
        """
        Initializes the APISpecMerger with the directory of spec files and the output file path.
        
        Args:
            spec_file_dir (str): Directory containing the API specification files.
            out_spec_file (str): Output file path for the merged API specification.
        """
        self.spec_file_dir = spec_file_dir
        self.out_spec_file = out_spec_file
        
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

"""
class SpecMerger:
    def __init__(self, spec_file_dir, out_spec_file):
        self.spec_file_dir = spec_file_dir
        self.out_spec_file = out_spec_file

    # Merge paths and component schemas
    def merge_dict(self, dest, src):
        for key, value in src['paths'].items():
            if key not in dest['paths']:
                dest['paths'][key] = value
        if 'components' in src.keys():
            for key, value in src['components']['schemas'].items():
                if key not in dest['components']['schemas']:
                    dest['components']['schemas'][key] = value

    def merge_specs(self):
        try:
            if os.path.exists(self.out_spec_file):
                os.remove(self.out_spec_file)
            basic_config_file = os.path.join(self.spec_file_dir, "static_page.yaml")

            final_spec = dict()
            final_spec['paths'] = dict()
            final_spec['components'] = dict()
            final_spec['components']['schemas'] = dict()
            #for file_name in OrderedList:
            for file_name in os.listdir(self.spec_file_dir):
                if file_name.endswith('.yaml') or file_name.endswith('.yml'):
                    print(f"FileName: {self.spec_file_dir}/{file_name}")
                    if file_name in ["static_page.yaml", "ready_probe.yaml"]:
                        continue
                    with open(os.path.join(self.spec_file_dir, file_name)) as f:
                        new_spec = yaml.safe_load(f)
                        self.merge_dict(final_spec, new_spec)
            # Add basic configuration
            if os.path.exists(basic_config_file):
                with open(basic_config_file) as fh:
                    new_spec = yaml.safe_load(fh)
                    final_spec.update(new_spec)
            else:
                print(f"basic_config_file does not exists {basic_config_file}")
            # Create Final Spec
            final_spec1 = json.loads(json.dumps(final_spec))
            with open(self.out_spec_file, mode='w') as n:
                yaml.safe_dump(final_spec1, n)
        except Exception as e:
            terr = traceback.format_exc()
            print(f"Error: {e} Traceback: {terr}")

"""
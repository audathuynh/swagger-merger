import collections
import io
import os
import sys
import yaml

def _main_():
    if len(sys.argv) < 2: 
        print("Usage: python3 swagger-merger.py <path-to-swagger-yaml-index-file>")
        return 0
    print("Start processing...") 
    input_file_path = sys.argv[1]

    with open(input_file_path, 'r') as input_file:
        try:
            data = yaml.safe_load(input_file)
        except yaml.YAMLError as exc:
            print(exc)

    dir_path = os.path.dirname(os.path.realpath(input_file_path))
    output_data = merge_refs(data, dir_path)

    print("Writing results into output file...")
    with io.open('output.yaml', 'w', encoding='utf8') as output_file:
        yaml.dump(output_data, output_file, default_flow_style=False, allow_unicode=True)
    print("Done.")

def merge_refs(data, working_dir):
    if '$ref' in data:
        yaml_path = data['$ref']
        if yaml_path.startswith('#'):
            return data
        nested_file_path = os.path.join(working_dir, yaml_path)
        nested_data = yaml.safe_load(open(nested_file_path, 'r'))
        return merge_refs(nested_data, os.path.dirname(nested_file_path))
    else:
        result = {}
        for k, v in data.items():
            if isinstance(v, collections.Mapping):
                child_data = merge_refs(v, working_dir)
                result[k] = child_data
            else:
                result[k] = v
        return result

_main_()
import sys
import ruamel.yaml as yaml
import collections
from configobj import ConfigObj


def convert_properties_to_yaml():
    # Read the file name from command line argument
    input_file = sys.argv[1]
    # Read key=value property configs in python dictionary
    config_dict = ConfigObj(input_file)
    # Store the result in yaml_dict
    yaml_dict = {}

    for key, value in config_dict.items():
        config_keys = key.split(".")

        for config_key in reversed(config_keys):
            value = {config_key: value}

        yaml_dict = update_dict(yaml_dict, value)

    # Write resultant dictionary to the yaml file
    yaml_file = open(input_file + '.yaml', 'w')
    yaml.dump(yaml_dict, yaml_file, Dumper=yaml.RoundTripDumper)


# Based on http://stackoverflow.com/a/3233356
def update_dict(original_dict, updated_dict):
    for k, v in updated_dict.items():
        if isinstance(v, collections.Mapping):
            r = update_dict(original_dict.get(k, {}), v)
            original_dict[k] = r
        else:
            original_dict[k] = updated_dict[k]
    return original_dict


convert_properties_to_yaml()

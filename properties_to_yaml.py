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
def update_dict(d, u):
    try:
        collectionsAbc = collections.abc
    except:
        collectionsAbc = collections
    for k, v in six.iteritems(u):
        dv = d.get(k, {})
        if not isinstance(dv, collectionsAbc.Mapping):
            d[k] = v
        elif isinstance(v, collectionsAbc.Mapping):
            d[k] = update_dict(dv, v)
        else:
            d[k] = v
    return d

''' Multipurpose configurator '''

__author__ = "Raul Farkas"

import json
import os


class obj(object):
    ''' Create an object based on a given dict'''

    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(
                   x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)


def file_exists(file):
    ''' Check if file exists in given directory'''
    exists = False
    for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name == file:
                    exists = True

    return exists


def check_configuration_validity(config_data):
    ''' Check if the basic configuration structure is valid'''
    valid = False
    if("profiles" in config_data.__dict__.keys() and "selected_profile" in config_data.__dict__.keys()):
        if ("default" in config_data.profiles.__dict__.keys()):
            valid = True
        else:
            print("The configuration file is missing the default profile!")
    else:
        print("The configuration file does not have the correct structure!")

    return valid


def configure(file_name):
    ''' Load selected profile and return it after checking its validity'''
    config_data = None
    return_profile = None
    if(file_exists(file_name)):
        print("Configuration file does not exist!")
    else:
        with open(file_name, "r") as f:
            config_data = json.load(f)

        config_data = obj(config_data)
        if(check_configuration_validity(config_data)):
            profiles = config_data.profiles
            if(config_data.selected_profile in config_data.profiles.__dict__.keys()):
                if config_data.selected_profile == "default":
                    raise Exception(
                        "The profile you chose is the defualt one, please select or create another one!")
                return_profile = getattr(
                    config_data.profiles, config_data.selected_profile)

    return return_profile


def generate_config_structure(file_name):
    ''' Generate basic config file with the default structure'''
    data = {"profiles": {"default": {}}, "selected_profile": "default"}
    try:
        with open(file_name, "w") as f:
            f.write(json.dumps(data, sort_keys=True,
                               indent=4, separators=(',', ': ')))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    ''' Example usage of the configurator '''
    conf = configure("config.json")
    print("User: %s\nPassword: %s\nHost: %s\nDatabase: %s" %
          (conf.db.user, conf.db.password, conf.db.host, conf.db.database))

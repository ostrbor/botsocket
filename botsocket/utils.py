import json
from .exceptions import (RequestFormatError, SettingsImproperlyConfigured)


def bin2dict(byte_str):
    """ Convert byte string -> string with json -> dict """
    string = byte_str.decode()
    try:
        dictionary = json.loads(string)
    except json.JSONDecodeError as e:
        raise RequestFormatError('Cant convert byte string to json', e)
    return dictionary

def dict2bin(dictionary):
    """ Convert dict -> string with json -> byte string """
    string = json.dumps(dictionary)
    return string.encode()

def compare_vars(template, target):
    """Check upper case variables from template module present in target module"""
    vars = [x for x in dir(template) if x.isupper()]
    for var in vars:
        if not hasattr(target, var):
            msg = 'Variable %s is absent in %s' % (var, target.__file__)
            raise SettingsImproperlyConfigured(msg)

import json
from .exceptions import RequestFormatError

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

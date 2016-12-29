"""Schema of messages send from client to server. """

error_schema = {
    'error_msg': {'type': 'string'},
}

command_schema = {
    'name': {'type': 'string',
             'required': True,
             'allowed': ['login', 'placebet'],
             'empty': False},
    'object': {'type': 'command',
               'required': True},
    'params': {'type': 'dict',
               'required': True, }
}

login_params_schema = {
    'user': {'type': 'string',
             'required': True,
             'empty': False},
    'password': {'type': 'string',
                 'required': True,
                 'empty': False},
    'url': {'type': 'string',
            'required': True,
            'empty': False},
}

placebet_params_schema = {
    'credentials': {'type': 'string',
                    'required': True,
                    'empty': False},
    'url': {'type': 'string',
            'required': True,
            'empty': False},
    'xpath': {'type': 'string',
              'required': True,
              'empty': False},
    'betsum': {'type': 'integer',
               'required': True, },
    'currency': {'type': 'string',
                 'required': True,
                 'empty': False},
}

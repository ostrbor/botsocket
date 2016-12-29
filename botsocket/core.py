import logging
import jsonpickle
from cerberus import DocumentError, SchemaError
from .validators import (command_validator, login_params_validator,
                         placebet_params_validator)
from .exceptions import CommandValidationError

logger = logging.getLogger(__name__)


def validate_command(command):
    if not command_validator.validate(command):
        raise CommandValidationError('Command structure is not valid: %s' %
                                     command)
    params = command['params']
    if command['name'] == 'login':
        if not login_params_validator.validate(params):
            raise CommandValidationError('Params of command %s are not valid' %
                                         command)
    elif command['name'] == 'placebet':
        if not placebet_params_validator.validate(params):
            raise CommandValidationError('Params of command %s are not valid' %
                                         command)


def run_command(binary_request):
    """ : binary request -> run command and return it's value """
    command = jsonpickle.decode(binary_request.decode())
    try:
        validate_command(command)
    except CommandValidationError as e:
        logger.exception(e)
        return str(e)
    else:
        command = command['object']
        result = command.run(**command['params'])
        return result

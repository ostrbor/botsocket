"""Command format: {'command_id': 'login', 'command': <obj of class Command>,
'params': {...}}"""
from cerberus import Validator
from .schemas import command_schema, login_params_schema, placebet_params_schema


class CommandValidator(Validator):
    def _validate_type_command(self, value):
        """ Enables validation for `command` schema attribute.
        :param value: field value.
        """
        try:
            if value.__class__.__name__ == 'Command':
                if hasattr(value, 'run'):
                    return True
        except AttributeError:
            return False


command_validator = CommandValidator(command_schema)
login_params_validator = Validator(login_params_schema)
placebet_params_validator = Validator(placebet_params_schema)

import pytest
from unittest.mock import patch, MagicMock
from botsocket.utils import (_has_same_vars, _has_empty_vars)
from botsocket.core import validate_command, run_command
from botsocket.exceptions import (SettingsImproperlyConfigured,
                                  CommandValidationError, )

MSG_BIN = b'{"command": "run", "params": {}}'
MSG_BIN_REV = b'{"params": {}, "command": "run"}'
MSG = {"command": "run", "params": {}}

valid_settings = MagicMock()
valid_settings.VAR = 'Customized value'


def test_hase_same_vars():
    default_settings = MagicMock()
    default_settings.VAR = 'Some value'
    invalid_settings = MagicMock()
    invalid_settings.__file__ = ''
    with pytest.raises(SettingsImproperlyConfigured):
        _has_same_vars(default_settings, invalid_settings)
    assert None == _has_same_vars(default_settings, valid_settings)


def test_has_empty_vars():
    invalid_settings = MagicMock()
    invalid_settings.__file__ = ''
    invalid_settings.VAR = ''
    with pytest.raises(SettingsImproperlyConfigured):
        _has_empty_vars(invalid_settings)
    assert None == _has_empty_vars(valid_settings)


def test_validate_command():
    command = MagicMock()
    with patch('botsocket.core.command_validator') as mock_command_validator:
        mock_command_validator.validate = MagicMock(return_value=False)
        with pytest.raises(CommandValidationError):
            validate_command(command)
        mock_command_validator.validate = MagicMock(return_value=True)
        command.__getitem__.return_value = 'login'
        with patch('botsocket.core.login_params_validator') as mock_login:
            mock_login.validate = MagicMock(return_value=False)
            with pytest.raises(CommandValidationError):
                validate_command(command)
            mock_login.validate = MagicMock(return_value=True)
            command.__getitem__.return_value = 'placebet'
            with patch(
                    'botsocket.core.placebet_params_validator') as mock_placebet:
                mock_placebet.validate = MagicMock(return_value=False)
                with pytest.raises(CommandValidationError):
                    validate_command(command)

# @patch('botsocket.core.jsonpickle.decode')
# def test_run_command(command):
#     with pytest.raises(CommandValidationError):
#         run_command(b'')
    # with patch('botsocket.core.validate_command') as mock_validate:
    #     mock_validate.return_value = True
    #     command.__gititem__.return_value = command

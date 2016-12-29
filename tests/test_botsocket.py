import pytest
from unittest.mock import patch, MagicMock
from botsocket.core import validate_command, run_command
from botsocket.exceptions import (SettingsImproperlyConfigured,
                                  CommandValidationError, )


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

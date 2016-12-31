import pytest
from unittest.mock import MagicMock
from botsocket.utils import _has_same_vars, _has_empty_vars
from botsocket.exceptions import SettingsImproperlyConfigured

MSG_BIN = b'{"command": "run", "params": {}}'
MSG_BIN_REV = b'{"params": {}, "command": "run"}'
MSG = {"command": "run", "params": {}}

valid_settings = MagicMock()
valid_settings.VAR = 'Customized value'


def test_has_same_vars_raises_exc():
    default_settings = MagicMock()
    default_settings.VAR = 'Some value'
    invalid_settings = MagicMock()
    invalid_settings.__file__ = ''
    with pytest.raises(SettingsImproperlyConfigured):
        _has_same_vars(default_settings, invalid_settings)
    assert None == _has_same_vars(default_settings, valid_settings)


def test_has_empty_vars_raises_exc():
    invalid_settings = MagicMock()
    invalid_settings.__file__ = ''
    invalid_settings.VAR = ''
    with pytest.raises(SettingsImproperlyConfigured):
        _has_empty_vars(invalid_settings)
    assert None == _has_empty_vars(valid_settings)

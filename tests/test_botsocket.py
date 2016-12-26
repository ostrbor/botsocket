import pytest
from botsocket.utils import bin2dict, dict2bin, _has_same_vars, _has_empty_vars
from botsocket.server import process_request
import botsocket
from botsocket.exceptions import SettingsImproperlyConfigured

MSG_BIN = b'{"command": "run", "params": {}}'
MSG_BIN_REV = b'{"params": {}, "command": "run"}'
MSG = {"command": "run", "params": {}}


def test_bin2dict():
    assert MSG == bin2dict(MSG_BIN)


def test_dict2bin():
    assert MSG_BIN == dict2bin(MSG) or MSG_BIN_REV == dict2bin(MSG)


def test_process_request(monkeypatch):
    class Command:
        @staticmethod
        def run(params):
            return 'Success'

    monkeypatch.setattr(botsocket.server, 'import_module', lambda _: Command())
    assert 'Success' == process_request(MSG_BIN)


def test_hase_same_vars():
    class DefaultSettings:
        VAR = 'Some value'

    class ValidUserSettings:
        VAR = 'Customized value'

    class InvalidUserSettings:
        # VAR is absent
        __file__ = ''

    with pytest.raises(SettingsImproperlyConfigured):
        _has_same_vars(DefaultSettings, InvalidUserSettings)
    assert None == _has_same_vars(DefaultSettings, ValidUserSettings)


def test_has_empty_vars():
    class ValidSettings:
        VAR = 'Some value'

    class InvalidSettings:
        VAR = ''
        __file__ = ''

    with pytest.raises(SettingsImproperlyConfigured):
        _has_empty_vars(InvalidSettings)
    assert None == _has_empty_vars(ValidSettings)

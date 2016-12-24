import pytest
from botsocket.utils import bin2dict, dict2bin, compare_vars
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


def test_compare_vars():
    class Template:
        VAR = ''

    class SameTarget:
        VAR = ''

    class DifTarget:
        __file__ = ''

    with pytest.raises(SettingsImproperlyConfigured):
        compare_vars(Template, DifTarget)

    assert None == compare_vars(Template, SameTarget)

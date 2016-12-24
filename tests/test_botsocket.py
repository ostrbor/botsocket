import pytest
from botsocket.utils import bin2dict, dict2bin
import botsocket
from botsocket.server import _process_request

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
    monkeypatch.setattr(botsocket.server, 'commands', Command())
    assert 'Success' == _process_request(MSG_BIN)

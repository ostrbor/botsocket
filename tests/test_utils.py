import pytest
import jsonpickle
from unittest.mock import MagicMock
from botsocket.utils import (_has_same_vars, _has_empty_vars, bin2dict,
                             dict2bin, exc2bin)
from botsocket.exceptions import (SettingsImproperlyConfigured,
                                  BotSocketWrapperException,
                                  BotSocketBaseException)

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


def test_bin2dict_dict2bin_return_value():
    MSG = {'msg': 'message'}
    MSG_BIN = b'{"msg": "message"}'
    binary_msg = dict2bin(MSG)
    assert MSG_BIN == binary_msg
    result = bin2dict(binary_msg)
    assert MSG == result


def test_bin2dict_dict2bin_raise_exc():
    MSG = b'invalid msg'
    with pytest.raises(BotSocketWrapperException):
        bin2dict(MSG)
    with pytest.raises(BotSocketBaseException):
        dict2bin(MSG)

def test_exc2bin_return_value():
    exc = TypeError('error')
    assert b'{"error_msg": "TypeError: error"}' == exc2bin(exc)



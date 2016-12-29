from importlib import import_module
import os
from .exceptions import (BotSocketWrapperException,
                         SettingsImproperlyConfigured)
from . import default_settings


def _has_empty_vars(user_settings):
    """User settings module must contain non empty upper case variables """
    # Assume value can be converted to string.
    upper_case_vars = [x for x in dir(user_settings) if x.isupper()]
    empty_vars = [x for x in upper_case_vars
                  if str(getattr(user_settings, x)) == '']
    if empty_vars:
        msg = 'Empty variable(s) in %s: %s' % (user_settings.__file__,
                                               ', '.join(empty_vars))
        raise SettingsImproperlyConfigured(msg)


def _has_same_vars(default_settings, user_settings):
    """User_settings module must contain all upper case vars from
    default_settings module. """
    default_vars = set([x for x in dir(default_settings) if x.isupper()])
    user_vars = set([x for x in dir(user_settings) if x.isupper()])
    if not default_vars.issubset(user_vars):
        absent_vars = default_vars - user_vars
        msg = 'Absent variable(s) in %s: %s' % (user_settings.__file__,
                                                ', '.join(absent_vars))
        raise SettingsImproperlyConfigured(msg)


def get_settings_module():
    settings_env = os.environ.get('BOTSOCKET_SETTINGS_MODULE',
                                  'botsocket.default_settings')
    try:
        settings_module = import_module(settings_env)
    except ImportError:
        raise ImportError('Cant import %s' % settings_env)
    _has_same_vars(default_settings, settings_module)
    _has_empty_vars(settings_module)
    return settings_module

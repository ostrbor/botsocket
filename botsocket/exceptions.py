class BotSocketBaseException(Exception):
    """Base exception"""
    pass


class CommandNotFoundError(BotSocketBaseException):
    """Cant find command in commands.py """
    pass


class SettingsImproperlyConfigured(BotSocketBaseException):
    """Custom settings file doesn't have variables like default_settings has """
    pass


class BotSocketWrapperException(BotSocketBaseException):
    """Wrap exception"""

    def __init__(self, msg, original_exception):
        super().__init__(msg + '(: %s)' % original_exception)
        self.original_exception = original_exception

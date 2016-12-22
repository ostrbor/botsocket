class BotSocketError(Exception):
    """Base exception"""
    pass


class LanguageMissingError(BotSocketError, ValueError):
    """Set up LANGUAGE in settings.py"""
    pass


class SocketBindError(BotSocketError):
    """Wrapper exception around socket bind error"""

    def __init__(self, msg, original_exception):
        super().__init__(msg + '(: %s)' % original_exception)
        self.original_exception = original_exception


class CommandNotFoundError(BotSocketError):
    """Cant find command in LANGUAGE """
    pass

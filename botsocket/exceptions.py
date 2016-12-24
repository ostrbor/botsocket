class BotSocketBaseError(Exception):
    """Base exception"""
    pass


class BotSocketWrapperError(BotSocketBaseError):
    """Wrap exception"""

    def __init__(self, msg, original_exception):
        super().__init__(msg + '(: %s)' % original_exception)
        self.original_exception = original_exception


class LanguageMissingError(BotSocketBaseError, ValueError):
    """Set up LANGUAGE in settings.py"""
    pass


class SocketBindError(BotSocketWrapperError):
    """Wrap exception around socket bind error"""
    pass


class CommandNotFoundError(BotSocketBaseError):
    """Cant find command in commands.py """
    pass


class RequestFormatError(BotSocketWrapperError):
    """Request from socket can not be converted to json. """
    pass

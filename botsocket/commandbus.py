import inspect
from abc import ABC, abstractmethod
from .exceptions import CommandHandlerNotFound


class Resolver:
    """Retrieves validator class and handler class of
    command using naming conventions. """

    def validator_for(self, command):
        try:
            return getattr(
                self._getmodule(command),
                command.__class__.__name__ + 'Validator')
        except AttributeError:
            return None

    def handler_for(self, command):
        try:
            return getattr(
                self._getmodule(command),
                command.__class__.__name__ + 'Handler')
        except AttributeError:
            return None

    def _getmodule(self, command):
        return inspect.getmodule(command)


class Bus:
    def __init__(self, resolver=None):
        self.resolver = Resolver()

    def execute(self, command):
        validator_cls = self.resolver.validator_for(command)
        if validator_cls:
            validator_cls().validate(command)

        handler_cls = self.resolver.handler_for(command)
        if handler_cls is None:
            raise CommandHandlerNotFound('Unable to find handler for ' +
                                         command.__class__.__name__)
        return handler_cls().handle(command)


class Command(ABC):
    """Naming convention: <command name> + 'Command' """
    pass


class CommandHandler(ABC):
    """Naming convention: <command class name> + 'Handler' """

    @abstractmethod
    def handle(self):
        pass


class CommandValidator(ABC):
    """Naming convention: <command class name> + 'Validator' """

    @abstractmethod
    def validate(self):
        """Rais error to interrupt execute. """
        pass

# TODO: test Resolver, test raise exceptions.
from botsocket.commandbus import (Bus, Command, CommandHandler,
                                  CommandValidator)

class MyCommand(Command):
    def __init__(self, param):
        self.param = param

class MyCommandHandler(CommandHandler):
    def handle(self, command):
        return command.param

def test_bus_executes_handler():
    command = MyCommand('param')
    bus = Bus()
    assert 'param' == bus.execute(command)




botsocket
=========

Secure socket communication via botnet

>>> pip install botsocket

Based on Command Bus design pattern.

**myserver.py**

.. code:: python

    import os
    from botsocket.server import start_server
    from mycommands import *

    if __name__ == '__main__':
      start_server(listen_ip='0.0.0.0', port=PORT, allowed_host=CLIENT_IP)

**mycommands.py**

.. code:: python

    from botsocket.commandbus import Command, CommandHandler

    class MyCommand(Command):
      def __init__(self, msg):
        self.msg = msg

    class MyCommandHandler(CommandHandler):
      def handle(self, command):
          return command.msg

**myclient.py**

.. code:: python

    import os
    from botsocket.client import send_command
    from mycommands import MyCommand

    if __name__ == '__main__':
      cmd = MyCommand('yo')
      result = send_command(cmd, server_ip=SERVER_IP, port=PORT)

--------------

Notes for production:

- create self-signed certificate *cert.pem*;

>>> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

- create *logging.yml*;

- import all commands in myserver.py in order to unpickle command's objects.

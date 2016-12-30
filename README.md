# botsocket
Secure socket communication via botnet         

Default settings are valid only for localhost testing. 
Based on Command Bus design pattern.

myserver.py
```python
import os
from botsocket.server import start_server
from mycommands import *

if __name__ == '__main__':
  # uncomment for production
  # os.environ['BOTSOCKET_SETTINGS_MODULE'] = 'settings.py' 
  start_server()
```

mycommands.py
```python
from botsocket.commandbus import Command, CommandHandler

class MyCommand(Command):
  def __init__(self, msg):
    self.msg = msg
    
class MyCommandHandler(CommandHandler):
  def handle(self, command):
      return command.msg
```

myclient.py
```python
import os
from botsocket.client import send_command
from mycommands import MyCommand

if __name__ == '__main__':
  # uncomment for production
  # os.environ['BOTSOCKET_SETTINGS_MODULE'] = 'settings.py' 
  cmd = MyCommand('yo')
  result = send_command(cmd)
```
---
Notes: 
- create *settings.py* and make sure it has same variables as in botsocket.default_settings.py;
- create self-signed certificate *cert.pem*;
- create *logging.yml*;
- import all commands in myserver.py in order to unpickle command's objects.

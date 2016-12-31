"""Runs first. Export custom or default settings for use in other modules."""
import os
import logging.config
import yaml
from .exceptions import BotSocketWrapperException
from .utils import get_settings_module

settings = get_settings_module()

# Setup logger and check for cert file
try:
    with open(settings.LOG_FILE) as log_file:
        config = yaml.safe_load(log_file.read())
        logging.config.dictConfig(config)
except FileNotFoundError as e:
    raise BotSocketWrapperException('Cant open logging settings file: %s' %
                                    settings.LOG_FILE, e)
if not os.path.isfile(settings.CERT_FILE):
    raise BotSocketWrapperException('Cant find certificate file: %s' %
                                    settings.CERT_FILE)

# Can't import before settings definition.
# try wrapper to avoid flake8 warnings
try:
    from .server import start_server
    from .client import send_command
    __all__ = [start_server, send_command]
except Exception:
    raise

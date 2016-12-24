from importlib import import_module
import os
import logging.config
import yaml
from .exceptions import (LoggingSettingsNotFound, CertificateNotFound)
from .utils import compare_vars
from . import default_settings

# Settings can be customized by env variable or
# used default from current package
settings_env = os.environ.get('BOTSOCKET_MODULE_SETTINGS',
                              'botsocket.default_settings')
settings = import_module(settings_env)

# Check for exsistance of all needed vars in settings, raise error if not
compare_vars(default_settings, settings)

# Setup logger and check for cert file
try:
    with open(settings.LOG_FILE) as log_file:
        config = yaml.safe_load(log_file.read())
        logging.config.dictConfig(config)
except FileNotFoundError as e:
    raise LoggingSettingsNotFound('Cant open logging settings file: %s' %
                                  settings.LOG_FILE, e)
if not os.path.isfile(settings.CERT_FILE):
    raise CertificateNotFound('Cant find certificate file: %s' %
                              settings.CERT_FILE)

from .server import start_server
from .client import send_command

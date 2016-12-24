import logging.config
import yaml
from .settings import LOG_CONFIG

with open(LOG_CONFIG) as logfile:
    config = yaml.safe_load(logfile.read())
    logging.config.dictConfig(config)

from .server import start_server
from .client import send_command

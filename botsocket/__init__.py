import logging.config
import yaml
from .settings import LANGUAGE, LOG_CONFIG
from .exceptions import LanguageMissingError

import pdb; pdb.set_trace()

with open(LOG_CONFIG) as logfile:
    config = yaml.safe_load(logfile.read())
    logging.config.dictConfig(config)

if not LANGUAGE:
    raise LanguageMissingError('LANGUAGE in settings.py is empty!')

from .server import start_server
from .client import send_command

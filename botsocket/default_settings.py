"""Default settings used in case BOTSOCKET_MODULE_SETTINGS was not set. """

ALLOWED_HOST = '127.0.0.1'

# Specified here because used by server and client
PORT = 8888

# Number of additional connections in queue to
# hold and switch after current connection is processed.
CONNECTIONS_IN_QUEUE = 0

# Amount of bytes to fetch from socket
RECV = 1024

LOG_FILE = 'logging.yml'

# Self-signed certificate.
CERT_FILE = 'cert.pem'

# Commands that server and client use to speak.
# Client sends {'command': 'cmdname', 'params': 'args'}
# Server imports cmdname from COMMAND_MODULE and calls it with 'params'.
COMMAND_MODULE = 'commands'

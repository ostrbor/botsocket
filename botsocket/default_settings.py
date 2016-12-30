"""Default settings used in case BOTSOCKET_MODULE_SETTINGS was not set.
Variables must be either strings or ints."""

# Client needs it to connect
SERVER_HOST = '127.0.0.1'

# Server will reject all other HOSTs in HOST HEADER
ALLOWED_HOST = '127.0.0.1'

# Specified here because used by server and client
PORT = 8888

# Number of additional connections in queue to
# hold and switch after current connection is processed.
CONNECTIONS_IN_QUEUE = 0

# Amount of bytes to fetch from socket
BYTES_AMOUNT = 1024

LOG_FILE = 'logging.yml'

# Self-signed certificate.
CERT_FILE = 'cert.pem'

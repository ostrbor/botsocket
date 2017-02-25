SERVER_IP = '127.0.0.1'
LISTEN_IP = '0.0.0.0'
PORT = 8888
ALLOWED_HOSTS = ['*']  # '*' means all hosts are allowed

# Number of additional connections in queue to
# hold and switch after current connection is processed.
CONNECTIONS_IN_QUEUE = 0

# Amount of bytes to fetch from socket.
# It depends on TCP protocol and can be lower
# then asked but never bigger.
CHUNK_SIZE = 1024

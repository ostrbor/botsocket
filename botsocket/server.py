import logging
import pickle
import socket
import ssl

from .commandbus import Bus
from .exceptions import BotSocketBaseException, BotSocketWrapperException

LISTEN_IP = '0.0.0.0'
PORT = 8888
ALLOWED_HOSTS = ['*']  # '*' means all hosts are allowed

# Number of additional connections in queue to
# hold and switch after current connection is processed.
CONNECTIONS_IN_QUEUE = 0

BYTES_AMOUNT = 1024  # Amount of bytes to fetch from socket

logger = logging.getLogger(__name__)


def _event_handler(connection, recv, ip_address):
    request = connection.recv(recv)
    command = pickle.loads(request)
    msg = "Received %s: %s. From IP %s" % (
        command.__class__.__name__, command.command_description, ip_address)
    logger.info(msg)
    bus = Bus()
    try:
        result = bus.execute(command)
    except BotSocketBaseException as e:
        response = str(e)
        connection.sendall(pickle.dumps(response))
        msg = "Sent error of %s: %s" % (command.__class__.__name__, response)
        logger.error(msg)
    else:
        response = result if result else 'None'
        connection.sendall(pickle.dumps(response))
        msg = "Sent result of %s: %s" % (command.__class__.__name__, response)
        logger.info(msg)


def _event_loop(ssl_sock, allowed_hosts, recv):
    while True:
        try:
            connection, address = ssl_sock.accept()  # address = (IP, PORT)
        except ssl.SSLError as e:
            logger.exception(str(e))
            continue
        if address[0] in allowed_hosts or '*' in allowed_hosts:
            _event_handler(connection, recv, address[0])
        else:
            msg = 'Blocked IP: %s\tServer has allowed ip set to %s' % (
                address[0], allowed_hosts)
            logger.warn(msg)
        connection.close()


def start_server(listen_ip=LISTEN_IP,
                 port=PORT,
                 allowed_hosts=ALLOWED_HOSTS,
                 certfile='cert.pem'):
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(bot_sock, certfile=certfile)
    try:
        ssl_sock.bind((listen_ip, port))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(listen_ip, port)
        logger.exception(msg)
        raise BotSocketWrapperException(msg, e)
    ssl_sock.listen(CONNECTIONS_IN_QUEUE)
    _event_loop(ssl_sock, allowed_hosts, BYTES_AMOUNT)

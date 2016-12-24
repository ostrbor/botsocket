import ssl
import logging
import socket
from . import commands
from .settings import (HOST, PORT, RECV, ALLOWED_HOST, CONNECTIONS_IN_QUEUE)
from .exceptions import (SocketBindError, CommandNotFoundError,
                         RequestFormatError)
from .utils import bin2dict, dict2bin

logger = logging.getLogger(__name__)


def _process_request(binary_request):
    """ : binary request -> run command and return it's value
    Command must be in format {'command': 'some name', 'params': {...}}
    'some name' is imported from commands.py and called with **params. """
    request = bin2dict(binary_request)  # might raise JSON exception
    try:
        command = getattr(commands, request['command'])
    except AttributeError:
        raise CommandNotFoundError('Unknown command!')
    result = command(request['params'])
    return result


def start_server(host='0.0.0.0', port=8888, recv=1024):
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(bot_sock, certfile='cert.pem')
    try:
        ssl_sock.bind((host, port))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(host, port)
        logger.exception(msg)
        raise SocketBindError(msg, e)
    ssl_sock.listen(CONNECTIONS_IN_QUEUE)
    while True:
        try:
            connection, address = ssl_sock.accept()  # address = (IP, PORT)
        except ssl.SSLError as e:
            logger.exception(str(e))
            continue
        if address[0] == ALLOWED_HOST:
            binary_request = connection.recv(recv)
            try:
                response = _process_request(binary_request)
                logger.info('IP: %s, Request: %s, Response: %s' %
                            (address[0], binary_request, response))
            except (CommandNotFoundError, RequestFormatError) as e:
                response = str(e)
                logger.exception(response)
            connection.sendall(dict2bin(response))
        else:
            msg = 'IP: %s is not allowed!' % address[0]
            logger.warn(msg)
        connection.close()

from importlib import import_module
import ssl
import logging
import socket
from . import settings
from .exceptions import (SocketBindError, RequestFormatError,
                         CommandNotFoundError)
from .utils import bin2dict, dict2bin

SERVER_HOST = '0.0.0.0'
logger = logging.getLogger(__name__)


def process_request(binary_request):
    """ : binary request -> run command and return it's value
    Command must be in format {'command': 'some name', 'params': {...}} """
    request = bin2dict(binary_request)  # might raise JSON exception
    try:
        command_module = import_module(settings.COMMAND_MODULE)
    except ImportError as e:
        msg = 'Cant import %s' % settings.COMMAND_MODULE
        logger.exception(msg)
        raise
    try:
        command = getattr(command_module, request['command'])
    except AttributeError as e:
        msg = 'Unknown command!'
        logger.exception(msg)
        raise CommandNotFoundError(msg)
    result = command(request['params'])
    return result


def start_server(host=SERVER_HOST, recv=settings.RECV):
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(bot_sock, certfile=settings.CERT_FILE)
    try:
        ssl_sock.bind((host, settings.PORT))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(host, settings.PORT)
        logger.exception(msg)
        raise SocketBindError(msg, e)
    ssl_sock.listen(settings.CONNECTIONS_IN_QUEUE)
    while True:
        try:
            connection, address = ssl_sock.accept()  # address = (IP, PORT)
        except ssl.SSLError as e:
            logger.exception(str(e))
            continue
        if address[0] == settings.ALLOWED_HOST:
            binary_request = connection.recv(recv)
            try:
                response = process_request(binary_request)
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

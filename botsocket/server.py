from importlib import import_module
import ssl
import logging
import socket
from . import settings
from .exceptions import (BotSocketWrapperException,
                         BotSocketBaseException)
from .core import run_command
from .utils import bin2dict, dict2bin, exc2bin

logger = logging.getLogger(__name__)


def _event_handler(connection):
    try:
        binary_request = connection.recv(recv)
        request = bin2dict(binary_request)
        response = run_command(binary_request)
        logger.info('IP: %s, Request: %s, Response: %s' %
                    (address[0], binary_request, response))
    except BotSocketBaseException as e:
        response = dict2bin(exc2bin(e))
        logger.exception(response)
    connection.sendall(response)


def _event_loop(ssl_sock, recv):
    while True:
        try:
            connection, address = ssl_sock.accept()  # address = (IP, PORT)
        except ssl.SSLError as e:
            logger.exception(str(e))
            continue
        if address[0] == settings.ALLOWED_HOST:
            _event_handler(connection)
        else:
            msg = 'IP: %s is not allowed!' % address[0]
            logger.warn(msg)
        connection.close()


def start_server(server_ip='0.0.0.0', recv=settings.BYTES_AMOUNT):
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(bot_sock, certfile=settings.CERT_FILE)
    try:
        ssl_sock.bind((server_ip, settings.PORT))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(server_ip, settings.PORT)
        logger.exception(msg)
        raise BotSocketWrapperException(msg, e)
    ssl_sock.listen(settings.CONNECTIONS_IN_QUEUE)
    _event_loop(ssl_sock, recv)

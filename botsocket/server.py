import logging
import pickle
import socket
import ssl

import settings

from .commandbus import Bus
from .exceptions import BotSocketBaseException, BotSocketWrapperException

LISTEN_IP = '0.0.0.0'
PORT = 8888
ALLOWED_HOST = '127.0.0.1'
logger = logging.getLogger(__name__)


def _handle_request(binary_request):
    """: binary_request : -> binary_response """
    command = pickle.loads(binary_request)
    bus = Bus()
    try:
        result = bus.execute(command)
    except BotSocketBaseException as e:
        response = '500: ' + str(e)
    else:
        msg = result if result else 'None'
        response = '200: ' + msg
    return pickle.dumps(response)


def _event_handler(connection, recv, ip_address):
    request = connection.recv(recv)
    response = _handle_request(request)
    logger.info('IP: %s, Request: %s, Response: %s' %
                (ip_address, request, response))
    connection.sendall(response)


def _event_loop(ssl_sock, allowed_host, recv):
    while True:
        try:
            connection, address = ssl_sock.accept()  # address = (IP, PORT)
        except ssl.SSLError as e:
            logger.exception(str(e))
            continue
        if address[0] == allowed_host:
            _event_handler(connection, recv, address[0])
        else:
            msg = 'IP: %s is not allowed!' % address[0]
            logger.warn(msg)
        connection.close()


def start_server(listen_ip=LISTEN_IP, port=PORT, allowed_host=ALLOWED_HOST):
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(bot_sock, certfile=settings.CERT_FILE)
    try:
        ssl_sock.bind((listen_ip, port))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(listen_ip, port)
        logger.exception(msg)
        raise BotSocketWrapperException(msg, e)
    ssl_sock.listen(settings.CONNECTIONS_IN_QUEUE)
    _event_loop(ssl_sock, allowed_host, settings.BYTES_AMOUNT)

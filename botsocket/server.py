import logging
import socket
from .settings import (HOST, PORT, RECV, LANGUAGE, ALLOWED_HOST,
                       CONNECTIONS_IN_QUEUE)
from .exceptions import SocketBindError, CommandNotFoundError


def _parse_request(bstr):
    """ :byte string -> byte string of command
    extract command from request """
    return bstr.split(b' ')[0]


def _run_command(cmd):
    """ : byte str -> run cmd (result must be byte str) """
    if not LANGUAGE.get(cmd):
        raise CommandNotFoundError('Unknown command!')
    else:
        return LANGUAGE[cmd]()


def _host_is_valid(HOST):
    """ : str -> bool """
    return HOST == ALLOWED_HOST


def start_server():
    logger = logging.getLogger(__name__)
    bot_sock = socket.socket()
    bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        bot_sock.bind((HOST, PORT))
    except Exception as e:
        msg = 'Cant bind socket to {}:{}'.format(HOST, PORT)
        logger.exception(msg)
        raise SocketBindError(msg, e)
    bot_sock.listen(CONNECTIONS_IN_QUEUE)
    while True:
        client_connection, client_address = bot_sock.accept()
        if _host_is_valid(client_address[0]):
            request = client_connection.recv(RECV)
            cmd = _parse_request(request)
            try:
                result = _run_command(cmd)
                logger.info('Command: %s, Result: %s' % (cmd, result))
            except CommandNotFoundError as e:
                result = str(e).encode()
                logger.exception()
        else:
            msg = 'IP: %s is not allowed!' % client_address[0]
            result = msg.encode()
            logger.error(msg)
        client_connection.sendall(result)
        client_connection.close()

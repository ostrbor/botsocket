import ssl
import logging
import socket
import pickle
from . import settings

logger = logging.getLogger(__name__)


def send_command(command, server_host=settings.SERVER_HOST):
    sock = socket.socket()
    sock.connect((server_host, settings.PORT))
    ssl_sock = ssl.wrap_socket(sock, certfile=settings.CERT_FILE)
    request = pickle.dumps(command)
    ssl_sock.send(request)
    response = ssl_sock.recv(settings.BYTES_AMOUNT)
    logger.info(response)
    sock.close()

import ssl
import logging
import socket
from .utils import dict2bin
from . import settings

logger = logging.getLogger(__name__)

def send_command(server_host='127.0.0.1'):
    sock = socket.socket()
    sock.connect((server_host, settings.PORT))
    ssl_sock = ssl.wrap_socket(sock, certfile=settings.CERT_FILE)
    ssl_sock.send(dict2bin({'command': 'login', 'params': {}}))
    response = ssl_sock.recv(settings.BYTES_AMOUNT)
    logger.info(response)
    sock.close()

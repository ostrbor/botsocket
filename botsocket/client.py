import ssl
import logging
import socket
from .settings import PORT, RECV
from .utils import dict2bin

logger = logging.getLogger(__name__)

SERVER_HOST = '185.51.247.25'

def send_command():
    sock = socket.socket()
    sock.connect((SERVER_HOST, PORT))
    ssl_sock = ssl.wrap_socket(sock, certfile='cert.pem')
    ssl_sock.send(dict2bin({'command': 'login', 'params': {}}))
    response = ssl_sock.recv(RECV)
    # sock.send(dict2bin({'command': 'login', 'params': {}}))
    # response = sock.recv(RECV)
    logger.info(response)
    sock.close()

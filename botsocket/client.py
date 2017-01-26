import logging
import pickle
import socket
import ssl

import settings

PORT = 8888
SERVER_IP = '127.0.0.1'
logger = logging.getLogger(__name__)


def send_command(command, server_ip=SERVER_IP, port=PORT):
    sock = socket.socket()
    sock.connect((server_ip, port))
    ssl_sock = ssl.wrap_socket(sock, certfile=settings.CERT_FILE)
    request = pickle.dumps(command)
    ssl_sock.send(request)
    response = ssl_sock.recv(settings.BYTES_AMOUNT)
    logger.info(response)
    sock.close()

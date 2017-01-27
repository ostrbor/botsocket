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
    msg = "Sent %s: %s" % (command.__class__.__name__, command.params_to_log)
    logger.info(msg)
    response_bytes = ssl_sock.recv(settings.BYTES_AMOUNT)
    response = pickle.loads(response_bytes)
    msg = "Received: %s" % (response)
    logger.info(msg)
    sock.close()

import logging
import pickle
import socket
import ssl

PORT = 8888
SERVER_IP = '127.0.0.1'
BYTES_AMOUNT = 1024  # Amount of bytes to fetch from socket
logger = logging.getLogger(__name__)


def send_command(command, server_ip=SERVER_IP, port=PORT, certfile='cert.pem'):
    sock = socket.socket()
    sock.connect((server_ip, port))
    ssl_sock = ssl.wrap_socket(sock, certfile=certfile)
    request = pickle.dumps(command)
    ssl_sock.send(request)
    msg = "Sent %s: %s" % (command.__class__.__name__,
                           command.command_description)
    logger.info(msg)
    response_bytes = ssl_sock.recv(BYTES_AMOUNT)
    response = pickle.loads(response_bytes) if response_bytes else 'None'
    msg = "Received: %s" % (response)
    logger.info(msg)
    sock.close()
    return response

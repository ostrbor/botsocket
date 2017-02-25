import logging
import logging.config
import pickle
import socket
import ssl

import yaml

from .settings import PORT, SERVER_IP
from .utils import recv_by_chunks


def send_command(command,
                 server_ip=SERVER_IP,
                 port=PORT,
                 certfile='cert.pem',
                 logfile='logging.yml'):
    with open(logfile) as config:
        logging.config.dictConfig(yaml.load(config))
    logger = logging.getLogger(__name__)
    sock = socket.socket()
    sock.connect((server_ip, port))
    ssl_sock = ssl.wrap_socket(sock, certfile=certfile)
    request = pickle.dumps(command)
    ssl_sock.send(request)
    msg = "Sent %s: %s" % (command.__class__.__name__,
                           command.command_description)
    logger.info(msg)
    response_bytes = recv_by_chunks(ssl_sock)
    response = pickle.loads(response_bytes) if response_bytes else 'None'
    msg = "Received response with length %s" % len(response)
    logger.info(msg)
    sock.close()
    return response

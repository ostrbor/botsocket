import logging
import logging.config
import pickle
import socket
import ssl

import yaml

from .commandbus import Bus
from .exceptions import BotSocketBaseException, BotSocketWrapperException
from .settings import ALLOWED_HOSTS, CONNECTIONS_IN_QUEUE, LISTEN_IP, PORT
from .utils import recv_by_chunks, send_by_chunks


class Server:
    def __init__(self,
                 listen_ip=LISTEN_IP,
                 port=PORT,
                 allowed_hosts=ALLOWED_HOSTS,
                 certfile='cert.pem',
                 logfile='logging.yml'):
        self.allowed_hosts = allowed_hosts
        with open(logfile) as config:
            logging.config.dictConfig(yaml.load(config))
        self.logger = logging.getLogger(__name__)
        self.start_server(listen_ip, port, certfile)

    def start_server(self, listen_ip, port, certfile):
        bot_sock = socket.socket()
        bot_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssl_sock = ssl.wrap_socket(bot_sock, certfile=certfile)
        try:
            ssl_sock.bind((listen_ip, port))
        except Exception as e:
            msg = 'Cant bind socket to {}:{}'.format(listen_ip, port)
            self.logger.exception(msg)
            raise BotSocketWrapperException(msg, e)
        ssl_sock.listen(CONNECTIONS_IN_QUEUE)
        self._event_loop(ssl_sock)

    def _event_loop(self, ssl_sock):
        while True:
            try:
                connection, address = ssl_sock.accept()  # address = (IP, PORT)
            except ssl.SSLError as e:
                self.logger.exception(str(e))
                continue
            if address[0] in self.allowed_hosts or '*' in self.allowed_hosts:
                self._event_handler(connection, address[0])
            else:
                msg = 'Blocked IP: %s\tServer has allowed ip set to %s' % (
                    address[0], self.allowed_hosts)
                self.logger.warn(msg)
            connection.close()

    def _event_handler(self, connection, ip_address):
        request = recv_by_chunks(connection)
        command = pickle.loads(request)
        msg = "Received %s: %s. From IP %s" % (command.__class__.__name__,
                                               command.command_description,
                                               ip_address)
        self.logger.info(msg)
        bus = Bus()
        try:
            result = bus.execute(command)
        except BotSocketBaseException as e:
            response = str(e)
            connection.sendall(pickle.dumps(response))
            msg = "Sent error of %s: %s" % (command.__class__.__name__,
                                            response)
            self.logger.error(msg)
        else:
            response = result if result else 'None'
            data = pickle.dumps(response)
            send_by_chunks(connection, data)
            msg = "Sent result of %s. Data length is %s" % (
                command.__class__.__name__, len(data))
            self.logger.info(msg)

# coding = utf-8
import socket
from loguru import logger
from settings import listen_settings, mysql_settings

class Listener:
    
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = listen_settings['host']
        self.port = listen_settings['port']
        self.max_connection = listen_settings['max_connection']

    def listen(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_connection)
            logger.debug('Bind IP {} and Port {}'.format(self.host, self.port))
        except Exception as err:
            logger.error(str(err))

    def get_socket(self):
        return self.socket

    def destory(self):
        try:
            self.socket.close()
            logger.debug('listener socket destoryed')
        except Exception as err:
            logger.error(str(err))

class DBConnector:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = mysql_settings['host']
        self.port = mysql_settings['port']

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            logger.debug('Connected IP {} and Port {}'.format(self.host, self.port))
        except Exception as err:
            logger.error(str(err))

    def get_socket(self):
        return self.socket

    def destory(self):
        try:
            self.socket.close()
            logger.debug('connector socket destoryed')
        except Exception as err:
            logger.error(str(err))
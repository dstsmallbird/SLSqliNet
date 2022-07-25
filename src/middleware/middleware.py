# coding = utf-8
import time
import threading
from loguru import logger
from network import Listener, DBConnector

def query_handler(listen_channel, output_file):
    # connect to DB and generate DB connector
    db_connector = DBConnector()
    db_connector.connect()
    db_socket = db_connector.get_socket()

    # obtain init information from DB
    init_data = db_socket.recv(81920)
    logger.debug('Init Message: {}'.format(init_data))

    # send init information to client
    listen_channel.send(init_data)
    # wait for response from client
    time.sleep(0.01)
    f = open(output_file, 'a')
    
    while True:
        try:
            # get client response, data format: Bytes
            query_data = listen_channel.recv(81920)
            # destroy DB connector
            if (query_data == b''):
                f.close()
                db_connector.destory()
                return
            # DB connector sends data to DB
            logger.debug('Query: {}'.format(query_data))
            f.write(query_data.decode('gb18030', 'ignore') + '\n')
            db_socket.send(query_data)
            time.sleep(0.01)
            # obtain information from DB
            ret_data = db_socket.recv(81920)
            logger.debug('Return: {}'.format(ret_data))
            # forward DB data to client
            listen_channel.send(ret_data)
        except Exception as e:
            logger.error(str(e))
            f.close()
            db_connector.destory()
            return

if __name__ == '__main__':
    listener = Listener()
    listener.listen()
    listen_socket = listener.get_socket()
    output_file = 'sql_web_app.txt'
    
    while True:
        try:
            listen_channel, remote_addr = listen_socket.accept()
            logger.debug('Remote Addr: {}'.format(remote_addr))
            handler = threading.Thread(target=query_handler, args=(listen_channel,output_file,))
            handler.start()
        except:
            listener.destory()
            exit(0)
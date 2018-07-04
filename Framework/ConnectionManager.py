import configparser
from Framework.Connection import Connection


class ConnectionManager:

    def __init__(self):
        self.connections = []
        self.__load_connections()

    def __load_connections(self):
        config = configparser.ConfigParser()
        config.read('connections.ini')
        for section in config.sections():
            connection = Connection(section, dict(config.items(section)))
            self.connections.append(connection)

    def print_connections(self):
        print('There are %d connections:' % len(self.connections))
        for connection in self.connections:
            print(connection)

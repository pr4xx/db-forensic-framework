import configparser
from framework.Connection import Connection


class ConnectionManager:

    def __init__(self, core):
        self.core = core
        self.connections = []
        self.__load_connections()

    def __load_connections(self):
        """ Reads and parses the Connectionfile file. """

        config = configparser.ConfigParser()
        config.read('Connectionfile')
        for section in config.sections():
            connection = Connection(section, dict(config.items(section)))
            self.connections.append(connection)

    def print_connections(self):
        """ Prints out a list of all loaded connections. """

        print('There are %d connections:' % len(self.connections))
        for connection in self.connections:
            print(connection)

    def get_connection(self, name):
        """ Returns a connection object for a given name. """

        for connection in self.connections:
            if connection.config['name'] == name:
                return connection

        raise Exception('Unknown connection name!')

    def get_connection_string(self, name):
        """ Builds and returns a connection string for a given connection name. """

        config = self.get_connection(name).config
        connection_type = config['type']
        if connection_type == 'mysql':
            host = config['host']
            port = config['port']
            database = config['database']
            username = config['username']
            password = config['password']
            return 'mysql+pymysql://' + username + ':' + password + '@' + host + ':' + port + '/' + database
        elif connection_type == 'sqlite':
            file = config['file']
            return 'sqlite:///' + file
        else:
            raise Exception('Connection type not supported!')


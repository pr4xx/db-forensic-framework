from pony.orm import Database
from framework.ConnectionManager import ConnectionManager
from framework.DatabaseIdentifier import DatabaseIdentifier
from framework.PluginManager import PluginManager


class Core:

    instance = None

    def __init__(self):
        self.connection_manager = ConnectionManager(self)
        self.plugin_manager = PluginManager(self)
        self.database_identifier = DatabaseIdentifier(self)
        self.connection = None
        self.db = Database()
        Core.instance = self

    def init(self, connection_name):
        if connection_name is not None:
            self.connection = self.connection_manager.get_connection(connection_name)
            self.connection_manager.bind_db(self.db, connection_name)
            self.db.generate_mapping()

    def result(self, result):
        pass
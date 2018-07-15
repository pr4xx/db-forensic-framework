from framework.ConnectionManager import ConnectionManager
from framework.DatabaseIdentifier import DatabaseIdentifier
from framework.PluginManager import PluginManager


class Core:

    def __init__(self):
        self.connection_manager = ConnectionManager(self)
        self.plugin_manager = PluginManager(self)
        self.database_identifier = DatabaseIdentifier(self)



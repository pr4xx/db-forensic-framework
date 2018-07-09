from Framework.ConnectionManager import ConnectionManager
from Framework.DatabaseIdentifier import DatabaseIdentifier


class Core:

    def __init__(self):
        self.connection_manager = ConnectionManager(self)
        self.database_identifier = DatabaseIdentifier(self)



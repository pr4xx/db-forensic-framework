from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from changanya.simhash import Simhash


class DatabaseIdentifier:

    def __init__(self, core):
        self.core = core

    def serialize_database(self, name):
        """ Returns a string containing a serialized database (tables and columns). """

        connection_string = self.core.connection_manager.get_connection_string(name)
        engine = create_engine(connection_string)
        inspector = reflection.Inspector.from_engine(engine)
        database_items = []
        for table_name in inspector.get_table_names():
            database_items.append(table_name)
            columns = inspector.get_columns(table_name)
            for column in columns:
                database_items.append(column['name'])

        return ','.join(database_items)

    def get_hash(self, name):
        """ Generates a similarity hash for a given connection name. """

        serialized_database = self.serialize_database(name)

        return Simhash(serialized_database)

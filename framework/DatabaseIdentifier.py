from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from changanya.simhash import Simhash


class DatabaseIdentifier:

    def __init__(self, core):
        self.core = core

    def serialize_database(self, name):
        """ Returns a string containing a serialized database (only columns). """

        connection_string = self.core.connection_manager.get_connection_string(name)
        engine = create_engine(connection_string)
        inspector = reflection.Inspector.from_engine(engine)
        database_items = []
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            for column in columns:
                database_items.append(column['name'])
        database_items.sort()

        return ' '.join(database_items)

    def get_hash(self, name):
        """ Generates a similarity hash for a given connection name. """

        serialized_database = self.serialize_database(name)

        return Simhash(serialized_database, hashbits=64)

    def print_guesses(self, name):
        """ Compares plugins and their similarity hashes for a given connection name. """

        plugin_found = False
        connection_hash = self.get_hash(name)
        for plugin in self.core.plugin_manager.plugins:
            plugin_hash = int(plugin.config['target']['sim_hash'])
            hash_object = Simhash('', hashbits=64)
            hash_object.hash = plugin_hash
            similarity = connection_hash.similarity(hash_object)
            if similarity > 0.75:
                plugin_found = True
                print("Found plugin {} with {:.1f}% similarity.".format(plugin.config['name'], similarity * 100))
        if not plugin_found:
            print("No matching plugin found")

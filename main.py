import click
from Framework.Core import Core

# Bootstrap the application
core = Core()


# Register commands and plugins
@click.group()
def cli():
    pass


@cli.command(name='connection:list')
def list_connections():
    """ Lists all connections. """

    core.connection_manager.print_connections()


@cli.command(name='connection:hash')
@click.argument('name')
def hash_connection(name):
    """ Returns a hash for a given connection name. """

    print(core.database_identifier.get_hash(name))


# Run the application
cli()

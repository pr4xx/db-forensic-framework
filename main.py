import click
from Framework.Core import Core

# Bootstrap the application
core = Core()


# Register commands and plugins
@click.group()
def cli():
    pass


@cli.command(name='list:connections')
def list_connections():
    core.connection_manager.print_connections()


# Run the application
cli()

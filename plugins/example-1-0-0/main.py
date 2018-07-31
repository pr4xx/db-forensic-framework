import click
from pony.orm import *
from framework.Core import Core

# Entity definitions


class Folder(Core.instance.db.Entity):
    _table_ = "folders"
    thread_key = PrimaryKey(str)

# Command definitions


@click.group()
@click.pass_context
def cli(ctx):
    """ Sample plugin description. """
    pass


@cli.command()
@click.pass_context
@db_session
def sync(ctx):
    Folder.select().show()
    pass


@cli.command()
@click.pass_context
def sync2(ctx):
    print(2)
    print(ctx.obj)
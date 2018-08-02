import click
from datetime import datetime
from pony.orm import *
from framework.Core import Core
from framework.analysis.timeline.Timeline import Timeline
from framework.analysis.timeline.TimelineElement import TimelineElement

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
    timeline = Timeline("my timeline")
    timeline.add(TimelineElement(datetime.now(), "header 1", "content 1"))
    timeline.add(TimelineElement(datetime.now(), "header 2", "content 2"))
    timeline.add(TimelineElement(datetime.now(), "header 3", "content 3"))
    print(timeline.to_json())


@cli.command()
@click.pass_context
def sync2(ctx):
    print(2)
    print(ctx.obj)
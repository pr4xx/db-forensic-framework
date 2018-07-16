import click


@click.group()
@click.pass_context
def cli(ctx):
    """ Sample plugin description. """
    pass

@cli.command()
@click.pass_context
def sync(ctx):
    print(1)
    print(ctx.obj)

@cli.command()
@click.pass_context
def sync2(ctx):
    print(2)
    print(ctx.obj)
from . import CommandFactory
import click
import inspect

command_factory = CommandFactory()

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['cli'] = click
    ctx.obj['debug'] = debug

@cli.command()
@click.pass_context
def compare(ctx, **args):
    args = {**args, **ctx.obj}
    command = command_factory.factory(command=inspect.currentframe().f_code.co_name, command_arguments=args)
    command.exec()

if __name__ == '__main__':
    cli()
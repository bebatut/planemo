"""Module describing the planemo ``training_fill_data_library`` command."""
import click

from planemo import options
from planemo.cli import command_function
from planemo.training import fill_data_library


@click.command('training_fill_data_library')
@options.optional_tools_arg(multiple=True, allow_uris=True)
@options.training_fill_data_library_options()
@command_function
def cli(ctx, uris, **kwds):
    """Build training template from workflow."""
    kwds["no_dependency_resolution"] = True
    print("test")
    fill_data_library(kwds, ctx)

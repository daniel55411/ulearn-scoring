import click


@click.group()
@click.version_option()
def cli():
    """Scoring of statements in ulearn by weeks"""


@cli.command(
    name='score',
    help=''
)
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")

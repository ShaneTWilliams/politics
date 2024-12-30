import sys

import click
from pol.targets import *


@click.group()
def cli():
    pass


def main():
    cli.add_command(build)
    cli.add_command(format_code, "format")
    cli.add_command(clean)
    cli.add_command(echo)

    try:
        ctx = cli.make_context("cli", sys.argv[1:])
        cli.invoke(ctx)
    except click.exceptions.Exit as exit_exception:
        if exit_exception.exit_code == 0:
            sys.exit(0)
        else:
            raise exit_exception

if __name__ == "__main__":
    main()

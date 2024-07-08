import shutil
import subprocess
import sys

import click
from pol.paths import ARTIFACT_DIR, PYTHON_PACKAGE_DIR, ROOT_DIR, WEB_ARTIFACT_DIR


def run_cmd(cmd, error, cwd=None):
    click.secho("Running", bold=True, nl=False)
    for text in cmd:
        if " " in str(text):
            click.secho(f' "{text}"', nl=False, underline=True)
        else:
            click.secho(f" {text}", nl=False, underline=True)
    if cwd is not None:
        click.secho(" in ", bold=True, nl=False)
        click.secho(cwd, underline=True, nl=False)
    click.secho("")

    with subprocess.Popen(cmd, cwd=cwd) as proc:
        if proc.wait() != 0:
            click.secho(error, bold=True, fg="red")
            sys.exit(1)


# web target should be:
# bun run build -- --watch


@click.command()
def build():
    from pol.elections.build import build

    build()

    WEB_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ARTIFACT_DIR, WEB_ARTIFACT_DIR, dirs_exist_ok=True)


@click.command()
def scratch():
    print(ROOT_DIR)


@click.command()
def serve_web():
    server_address = ("", 8000)
    # httpd = SimpleHTTPServer(server_address, BaseHTTPRequestHandler)
    # httpd.serve_forever()


@click.command()
def format_code():
    run_cmd(
        ["isort", "--profile=black", PYTHON_PACKAGE_DIR],
        "Failed to isort Python code",
    )
    run_cmd(["black", PYTHON_PACKAGE_DIR], "Failed to format Python code")
    click.secho("Successfully formatted Python code", bold=True, fg="green")

@click.command()
def label():
    import curses
    
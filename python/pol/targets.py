import subprocess
import sys

import click
from pol.paths import (
    ARTIFACT_DIR,
    GEOMETRY_ARTIFACT_DIR,
    PYTHON_DIR,
    PYTHON_PACKAGE_DIR,
    WEB_ARTIFACT_DIR,
    WEB_DIR,
)


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


@click.command()
@click.option("--target", type=click.Choice(["json", "web", "all"]))
def build(target):
    assert target is not None

    if target == "json" or target == "all":
        from pol.elections.build import build as json_build

        json_build()

    if target == "web" or target == "all":
        run_cmd(
            ["npm", "install"],
            "Failed to install web dependencies",
            cwd=WEB_DIR,
        )
        run_cmd(
            ["npm", "run", "build"],
            "Failed to build web artifacts",
            cwd=WEB_DIR,
        )


@click.command()
def format_code():
    run_cmd(
        ["isort", "--profile=black", PYTHON_PACKAGE_DIR],
        "Failed to isort Python code",
    )
    run_cmd(["black", PYTHON_PACKAGE_DIR], "Failed to format Python code")
    click.secho("Successfully formatted Python code", bold=True, fg="green")


@click.command()
def clean():
    for dir in [
        ARTIFACT_DIR,
        PYTHON_DIR / "pol.egg-info",
        PYTHON_PACKAGE_DIR / "__pycache__",
        PYTHON_PACKAGE_DIR / "elections/__pycache__",
        WEB_ARTIFACT_DIR,
        WEB_DIR / "build",
        WEB_DIR / "node_modules",
        WEB_DIR / ".vercel",
        WEB_DIR / ".svelte-kit",
        GEOMETRY_ARTIFACT_DIR,
    ]:
        run_cmd(
            ["rm", "-rf", dir],
            f"Failed to clean {dir}",
        )

    click.secho("Successfully cleaned artifacts", bold=True, fg="green")


@click.command()
def echo():
    click.echo(f"Politics!")

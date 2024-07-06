import shutil

import click

from pol.paths import ROOT_DIR, ARTIFACTS_DIR, WEB_ARTIFACTS_DIR


# web target should be:
# bun run build -- --watch

@click.command()
def build():
    from pol.build.build import build
    build()

    WEB_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ARTIFACTS_DIR, WEB_ARTIFACTS_DIR, dirs_exist_ok=True)


@click.command()
def scratch():
    print(ROOT_DIR)


@click.command()
def serve_web():
    server_address = ('', 8000)
    # httpd = SimpleHTTPServer(server_address, BaseHTTPRequestHandler)
    # httpd.serve_forever()

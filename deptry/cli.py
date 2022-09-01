import argparse
import logging
import sys

import click

from deptry.core import Core
from deptry.config import Config


@click.group()
def deptry():
    pass


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Print more output.")
@click.option("--ignore-dependencies", "-i", multiple=True, help="Dependencies listed in pyproject.toml that should be ignored, even if they are not imported.")
@click.option("--ignore-directories", "-id", multiple=True, help="Directories in which .py files should not be scanned for imports to determine if a dependency is used or not. Defaults to 'venv'. Specify multiple directories by using this flag twice, e.g. `-id .venv -id other_dir`")
def check(verbose, ignore_dependencies, ignore_directories):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, handlers=[logging.StreamHandler()], format="%(message)s")

    cli_arguments = {}
    if len(ignore_dependencies)>0:
        cli_arguments['ignore_dependencies'] = list(ignore_dependencies)
    if len(ignore_directories)>0:
        cli_arguments['ignore_directories'] = list(ignore_directories)

    config = Config(cli_arguments)

    obsolete_dependencies = Core(ignore_dependencies=config.config['ignore_dependencies']).run()
    if len(obsolete_dependencies):
        logging.info(f"pyproject.toml contains obsolete dependencies: {obsolete_dependencies}")
        exit(1)
    else:
        exit(0)


deptry.add_command(check)
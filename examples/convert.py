import json
from typing import Dict, IO, Union

import click
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@click.command()
@click.option(
    "--indent", type=int, default=4, help="The indent side for the output JSON"
)
@click.argument("source", type=click.File("r"))
def main(source, indent):
    "Convert a YAML file to pretty JSON"
    data = yaml.load(source, Loader=Loader)
    click.echo(json.dumps(data, indent=indent))


if __name__ == "__main__":
    main()

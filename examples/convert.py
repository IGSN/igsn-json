import json
from datetime import datetime, date

import click
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def datetime_handler(obj):
    "Seperate handler to handle datetimes -> JSON"
    return (
        obj.isoformat()
        if isinstance(obj, (datetime, date))
        else json.JSONEncoder().default(obj)
    )


@click.command()
@click.option(
    "--indent", type=int, default=4, help="The indent side for the output JSON"
)
@click.argument("source", type=click.File("r"))
def main(source, indent):
    "Convert a YAML file to pretty JSON"
    data = yaml.load(source, Loader=Loader)
    output = json.dumps(data, indent=indent, default=datetime_handler)
    click.echo(output)


if __name__ == "__main__":
    main()

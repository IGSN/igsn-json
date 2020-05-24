from pathlib import Path

import pytest
import jsonref as json
from fastjsonschema import compile as compile_schema


# Get the root directory of the project
ROOT = Path(__file__).parent.parent.absolute()
print(f"Schema root at {ROOT}")


@pytest.fixture()
def registration_schema_folder():
    "Get the location of the given schema folder."
    schema_version = "v0.1"
    return ROOT / f"schema.igsn.org/json/registration/{schema_version}/"


@pytest.fixture()
def geosample_schema_folder():
    schema_version = "v0.1"
    return ROOT / f"schema.igsn.org/json/description/geoSample/{schema_version}/"


@pytest.fixture()
def validator(registration_schema_folder):
    "Load up the registration validator."
    schema_file = registration_schema_folder / "core.schema.json"
    with open(schema_file, "r", encoding="utf-8") as src:
        # Here we're using jsonref to dereference local files for dev purposes
        # in production these will all need to be replaced with
        # dereferencable URIs
        schema = json.load(src, base_uri=schema_file.as_uri())
        return compile_schema(schema)

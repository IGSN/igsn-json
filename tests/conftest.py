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


def load_schema(folder, schema):
    "Load and compile a schema"
    schema_file = folder / schema
    with open(schema_file, "r", encoding="utf-8") as src:
        # Here we're using jsonref to dereference local files for dev purposes
        # in production these will all need to be replaced with
        # dereferencable URIs
        schema = json.load(src, base_uri=schema_file.as_uri())
        return compile_schema(schema)

@pytest.fixture()
def registration_validator(registration_schema_folder):
    "Load up the registration validator."
    return load_schema(registration_schema_folder, "core.schema.json")


@pytest.fixture()
def timestamp_validator(registration_schema_folder):
    "Load up timestamp validator"
    return load_schema(registration_schema_folder, "timestamp.schema.json")

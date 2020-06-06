from pathlib import Path

import pytest
import jsonref as json
from fastjsonschema import compile as compile_schema


# Get the root directory of the project
ROOT = Path(__file__).parent.parent.absolute()


@pytest.fixture()
def profiles():
    "Return profile locations"
    profiles = {
        "registration": "registration/v0.1",
        "geosample": "description/geoSample/v0.1",
    }

    # Add base URL and return
    return {key: f"schema.igsn.org/json/{value}" for key, value in profiles.items()}


# Parameters to point at a version of the schema
@pytest.fixture()
def schema_home():
    "Specifies the root schema URI"
    github = {
        "host": "https://raw.githubusercontent.com",
        "org": "IGSN",
        "repo": "igsn-json",
        "branch": "issue-9-Merge_in_context_jsonld_to_registration_schema",
    }
    return f"{github['host']}/{github['org']}/{github['repo']}/{github['branch']}"

@pytest.fixture()
def registration_schema_folder(profiles):
    return ROOT / profiles["registration"]


@pytest.fixture()
def geosample_schema_folder(profiles):
    return ROOT / profiles["geoSample"]


def load_schema(folder, schema):
    "Load and compile a schema"
    schema_file = folder / schema
    with open(schema_file, "r", encoding="utf-8") as src:
        # Here we're using jsonref to dereference local files for dev purposes
        # in production these will all need to be replaced with
        # dereferencable URIs
        schema = json.load(src, base_uri=schema_file.as_uri())
        return compile_schema(schema)


def load_remote_schema(base_uri, schema):
    "Load and compile a schema remotely"
    schema_uri = f"{base_uri}/{schema}"
    return json.load(schema_uri, jsonschema=True)


@pytest.fixture()
def registration_validator(registration_schema_folder):
    "Load up the registration validator."
    return load_schema(registration_schema_folder, "main.schema.json")


@pytest.fixture()
def remote_registration_validator(schema_home, profiles):
    "Load up a validator based on the remote schema"
    schema_uri = f"{schema_home}/{profiles['registration']}/main.schema.json"
    schema = json.load_uri(schema_uri, jsonschema=True)
    return compile_schema(schema)


@pytest.fixture()
def timestamp_validator(registration_schema_folder):
    "Load up timestamp validator"
    return load_schema(registration_schema_folder, "timestamp.schema.json")

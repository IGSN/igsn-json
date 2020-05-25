from pathlib import Path
import json

import fastjsonschema as jsonschema
import pytest

# Find all the JSON Schema files in the folder
SCHEMA_FOLDER = Path(__file__).parent.parent / "schema.igsn.org" / "json"
TO_CHECK = [
    # (id_name, schema folder)
    ("geoSample", SCHEMA_FOLDER / "description" / "geoSample" / "v0.1"),
    ("bioSample", SCHEMA_FOLDER / "description" / "bioSample" / "v0.1"),
    ("materialSample", SCHEMA_FOLDER / "description" / "materialSample" / "v0.1"),
    ("registration", SCHEMA_FOLDER / "registration" / "v0.1"),
]

# Remap IDs and schemas so we can make tests a bit easier to follow
IDS, SCHEMAS = [], []
for short, directory in TO_CHECK:
    schemas = list(directory.glob("*.schema.json"))
    IDS.extend([short + ":" + schema.stem.split(".")[0] for schema in schemas])
    SCHEMAS.extend(schemas)


def test_folders_exist():
    assert SCHEMA_FOLDER.exists()


@pytest.mark.parametrize("schema", SCHEMAS, ids=IDS)
def test_schemas_exist(schema):
    assert schema.exists()


@pytest.mark.parametrize("schema", SCHEMAS, ids=IDS)
def test_schema_compiles(schema):
    # Load up schema
    assert schema.exists()
    with open(schema, "rb") as source:
        data = json.load(source)

    # Check that we've got a valid schema
    try:
        jsonschema.compile(data)
    except jsonschema.JsonSchemaDefinitionException as exc:
        msg = f"Schema {schema} failed to compile.\n\n"
        msg += f"Error was:\n{exc.message}"
        raise AssertionError(msg)


if __name__ == '__main__':
    pytest.main()

# Design some examples
import pytest
import jsonref as json
from fastjsonschema import compile as compile_schema, JsonSchemaException


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


@pytest.mark.parametrize(
    "obj,should_pass",
    [
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {
                    "name": "Jess Robertson",
                    "identifiers": [
                        {"kind": "orcid", "id": "0000-0002-4553-9697"},
                        {"kind": "researcherId", "id": "I-4625-2012"},
                    ],
                },
            },
            True,
        ),
        ({"igsn": "https://igsn.org/XXXTEST234"}, False),
        ({"registrant": {"name": "jess"}}, False),
        ({"igsn": "https://igsn.org/XXXTEST234", "registrant": "jess"}, False),
        ({"igsn": "https://igsn.org/XXXTEST234", "registrant": {"name": "jess"}}, True),
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {"name": "jess", "identifiers": []},
            },
            True,
        ),
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {"name": "jess"},
                "related": [],
            },
            True,
        ),
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {"name": "jess"},
                "related": ["foo"],
            },
            False,
        ),
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {"name": "jess"},
                "related": [
                    {"kind": "igsn", "id": "FOOTEST235", "relationship": "isPartOf"}
                ],
            },
            True,
        ),
        (
            {
                "igsn": "https://igsn.org/XXXTEST234",
                "registrant": {"name": "jess"},
                "related": [
                    {"kind": "igsn", "id": "FOOTEST235", "relationship": "isPartOf"},
                    {
                        "kind": "orcid",
                        "id": "0000-0002-4553-9697",
                        "relationship": "isCitedBy",
                    },
                ],
            },
            True,
        ),
    ],
)
def test_igsn_registration(validator, obj, should_pass):
    "Sanity checking for basic IGSN registration inputs."
    try:
        validator(obj)
        if not should_pass:
            raise AssertionError(f"Object {obj} unexpectedly validated")
    except JsonSchemaException as err:
        if should_pass:
            raise AssertionError(
                f"Object {obj} failed to validate. Error is {err.message}"
            )

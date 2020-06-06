# Design some examples
import pytest
from fastjsonschema import JsonSchemaException

# Some bogus data for testing - as (obj, is_valid) tuples
TEST_OBJECTS = [
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
]


@pytest.mark.parametrize("obj,should_pass", TEST_OBJECTS)
def test_igsn_registration(
    schema_home, profiles, registration_validator, obj, should_pass
):
    "Sanity checking for basic IGSN registration inputs."
    try:
        # Inject required IGSN registration context
        location = f"{schema_home}/{profiles['registration']}"
        obj["@context"] = f"{location}/context.jsonld"
        obj['@id'] = "https://example-agent.org/igsns/XXXTEST234"

        # Check validation (or not...)
        registration_validator(obj)
        if not should_pass:
            raise AssertionError(f"Object {obj} unexpectedly validated")
    except JsonSchemaException as err:
        if should_pass:
            raise AssertionError(
                f"Object {obj} failed to validate. Error is {err.message}"
            )


@pytest.mark.parametrize("obj,should_pass", TEST_OBJECTS)
def test_against_remote_schema(
    schema_home, profiles, remote_registration_validator, obj, should_pass
):
    "Check against remote schema for the branch"
    try:
        # Inject required IGSN registration context
        location = f"{schema_home}/{profiles['registration']}"
        obj["@context"] = f"{location}/context.jsonld"

        # Check validation (or not...)
        remote_registration_validator(obj)
        if not should_pass:
            raise AssertionError(f"Object {obj} unexpectedly validated")
    except JsonSchemaException as err:
        if should_pass:
            raise AssertionError(
                f"Object {obj} failed to validate. Error is {err.message}"
            )

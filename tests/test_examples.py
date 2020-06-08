import json
from datetime import date, datetime

from fastjsonschema import JsonSchemaException
import pytest
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from helpers.examples import json_examples, filenames

# Unwrap all our JSON files into seperate documents
JSON_DOCUMENTS = json_examples()


@pytest.mark.parametrize(
    "name,document", JSON_DOCUMENTS.items(), ids=JSON_DOCUMENTS.keys()
)
def test_json_validates_registration(registration_validator, name, document):
    "Examples should validate against our schema"
    # Check validation, wrap in some extra info if required
    try:
        registration_validator(document)
    except JsonSchemaException as exc:
        msg = f"Document {name}.json failed to validate.\n\nError was:\n{exc.message}"

        # Add in the value and rule for debugging purposes
        msg += "\nBad value is:\n" + json.dumps(exc.value, indent=4)
        msg += "\n...at path: " + str(exc.path)
        msg += f"\nRule is {exc.rule}:\n" + json.dumps(exc.rule_definition, indent=4)

        raise ValueError(msg)


# Include our conversion code here
def datetime_handler(obj):
    "Seperate handler to handle YAML datetimes -> JSON"
    return (
        obj.isoformat()
        if isinstance(obj, (datetime, date))
        else json.JSONEncoder().default(obj)
    )


@pytest.mark.parametrize(
    "yaml_file, json_file", zip(filenames("yaml"), filenames("json")), ids=filenames()
)
def test_yaml_json_equal(yaml_file, json_file):
    "The YAML and JSON versions should be the same..."
    # Sanity check yaml data
    yaml_file = yaml_file
    assert yaml_file.exists()
    with open(yaml_file, "r") as source:
        documents = list(yaml.load_all(source, Loader=Loader))
        yaml_json_str = json.dumps(
            documents[0] if len(documents) == 1 else documents, default=datetime_handler
        )

    # Load and serialize JSON to remove pretty-printing
    json_file = json_file
    assert json_file.exists()
    with open(json_file, "rb") as source:
        data = json.load(source)
        assert data
        json_str = json.dumps(data)

    # Check the two are the same
    assert json_str == yaml_json_str


if __name__ == "__main__":
    pytest.main()

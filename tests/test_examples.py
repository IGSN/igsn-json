from pathlib import Path
from collections import defaultdict
import json
from datetime import date, datetime

from fastjsonschema import JsonSchemaException
import pytest
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Example files from examples folder
EXAMPLES = Path(__file__).parent.parent / "examples"

# The example files are those for which we have both a JSON and YAML file
FILES = defaultdict(list)
for fname in EXAMPLES.iterdir():
    FILES[fname.stem].append(fname.suffix)
FILENAMES = [name for name, ext in FILES.items() if set(ext) == {".yaml", ".json"}]
YAML_FILES = [f"{fname}.yaml" for fname in FILENAMES]
JSON_FILES = [f"{fname}.json" for fname in FILENAMES]

# Unwrap all our JSON files into seperate documents
JSON_DOCUMENTS = {}
for jfile in JSON_FILES:
    name = jfile.split('.')[0]
    with open(EXAMPLES / jfile, "rb") as source:
        data = json.load(source)

    if isinstance(data, list):
        for idx, document in enumerate(data):
            JSON_DOCUMENTS[f"{name}[{idx}]"] = document
    else:
        JSON_DOCUMENTS[name] = data


@pytest.mark.parametrize("name,document", JSON_DOCUMENTS.items())
def test_json_validates(registration_validator, name, document):
    "Examples should validate against our schema"
    # Check validation, wrap in some extra info if required
    try:
        registration_validator(document)
    except JsonSchemaException as exc:
        raise ValueError(f'Document {name}.json failed to validate.\n\nError was:\n{exc.message}')


# Include our conversion code here
def datetime_handler(obj):
    "Seperate handler to handle YAML datetimes -> JSON"
    return (
        obj.isoformat()
        if isinstance(obj, (datetime, date))
        else json.JSONEncoder().default(obj)
    )


@pytest.mark.parametrize("yaml_file, json_file", zip(YAML_FILES, JSON_FILES))
def test_yaml_json_equal(yaml_file, json_file):
    "The YAML and JSON versions should be the same..."
    # Sanity check yaml data
    yaml_file = EXAMPLES / yaml_file
    assert yaml_file.exists()
    with open(yaml_file, "r") as source:
        documents = list(yaml.load_all(source, Loader=Loader))
        yaml_json_str = json.dumps(
            documents[0] if len(documents) == 1 else documents, default=datetime_handler
        )

    # Load and serialize JSON to remove pretty-printing
    json_file = EXAMPLES / json_file
    assert json_file.exists()
    with open(json_file, "rb") as source:
        data = json.load(source)
        assert data
        json_str = json.dumps(data)

    # Check the two are the same
    assert json_str == yaml_json_str

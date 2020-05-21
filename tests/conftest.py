from pathlib import Path

import pytest

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

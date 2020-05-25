import pytest
import fastjsonschema as jsonschema


@pytest.mark.parametrize("string", ["2020-12-01"])
def test_should_pass(timestamp_validator, string):
    "These strings should validate"
    timestamp_validator(string)


@pytest.mark.parametrize(
    "string",
    [
        "12-01-2020",
        "2020-13-01",
        "2012",
        "2012-32",
        "200905",
        "2009367",
        "2009-",
        "2007-04-05T24:50",
        "2009-000",
        "2009-M51",
        "2009M511",
        "2009-05-19T14a39r",
        "2009-05-19T14:3924",
        "2009-0519",
        "2009-05-1914:39",
        "2009-05-19 14:",
        "2009-05-19r14:39",
        "2009-05-19 14a39a22",
        "200912-01",
        "2009-05-19 14:39:22+06a00",
        "2009-05-19 146922.500",
        "2010-02-18T16.5:23.35:48",
        "2010-02-18T16:23.35:48",
        "2010-02-18T16:23.35:48.45",
        "2009-05-19 14.5.44",
        "2010-02-18T16:23.33.600",
        "2010-02-18T16,25:23:48,444",
    ],
)
def test_should_fail(timestamp_validator, string):
    "These strings shouldn't validate"
    with pytest.raises(jsonschema.JsonSchemaException):
        timestamp_validator(string)

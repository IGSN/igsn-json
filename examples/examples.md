# Examples

These are examples of simple JSON documents to give you an intuitive feel for how they should be structured.

We provide the examples in YAML so that they're easier to read (and because JSON doesn't support comments), but you can convert these to JSON with the Python script pretty easily:

```bash
$ python convert.py minimal_registration.yaml
{
    "@context": "http://schema.igsn.org/json/registration/v0.1/context.jsonld",
    "igsn": {
        "kind": "igsn",
        "id": "XXXCSIRO0001"
    },
    "registrant": {
        "name": "CSIRO",
        "identifiers": [
            {
                "kind": "orcid",
                "id": "0001-0001-0001-0001"
            },
            {
                "kind": "viaf",
                "id": "https://csiro.au/path/to/viaf.file"
            },
            {
                "kind": "uri",
                "id": "https://csiro.au"
            }
        ]
    }
}
```

which should also play nicely with other Unix-y tools

```bash
$ python convert.py minimal_registration.yaml | jq '.registratnt.identifiers[].kind'
"orcid"
"viaf"
"uri"
```

## Core IGSN Metadata



## Custom data about a sample

The `data` key can contain any extra information about a sample

### Basic data (without JSON-LD)

### Semantic context from JSON-LD

- Pointing to another JSON-LD 
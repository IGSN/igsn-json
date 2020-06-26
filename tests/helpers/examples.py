from pathlib import Path
import json
from collections import defaultdict

# Example files from examples folder
EXAMPLES = Path(__file__).parent.parent.parent / "examples"


def filenames(extension=None):
    """
    Returns all the example files from the examples directory

    Example files have both a JSON and YAML extension
    """
    files = defaultdict(list)
    for fname in EXAMPLES.iterdir():
        files[fname.stem].append(fname.suffix)
    names = [name for name, ext in files.items() if set(ext) == {".yaml", ".json"}]

    # Wrap in extension if required
    if extension is not None:
        return [EXAMPLES / f"{name}.{extension}" for name in names]
    else:
        return names


def json_examples():
    "Get all the JSON-formatted example data"
    docs = {}
    for name, jfile in zip(filenames(), filenames("json")):
        with open(jfile, "rb") as source:
            data = json.load(source)

        if isinstance(data, list):
            for idx, document in enumerate(data):
                docs[f"{name}_doc_{id}"] = document
        else:
            docs[name] = data
    return docs

# Examples

These are examples of simple JSON documents to give you an intuitive feel for how they should be structured. This is a proposal at this stage and as such is designed ot be a strawman to start discussion. If you don't like something here then please raise it in the [discussion board](https://github.com/orgs/IGSN/teams/igsn-2040-sprint).

We provide the examples in YAML so that they're easier to read (and because JSON doesn't support comments), but you can convert these to JSON with the Python script pretty easily:

```bash
$ python convert.py minimal_registration.yaml
{
    "@context": "http://schema.igsn.org/json/registration/v0.1/context.jsonld",
    "igsn": {
        "kind": "igsn",
        "id": "XXXCSIRO0001"
    },
# snip...
```

which should also play nicely with other Unix-y tools

```bash
$ python convert.py minimal_registration.yaml | jq '.registratnt.identifiers[].kind'
"orcid"
"viaf"
"uri"
```

You need to install click and pyyaml for this to work. You can get all of these using the Pipfile in the root directory:

```bash
$ cd path/to/igsn_json
$ pipenv install  # or pipenv install --dev for all the dev tools
Installing dependencies from Pipfile.lock (e3dedb)…
  ============================---- 8/9 - 00:00:05
...
```

Once installed, you can run the scripts in an isolated environment with the `pipenv shell` command.

```bash
$ pipenv shell
Launching subshell in virtual environment...
# do whatever you were going to do in the new shell
```

Let's walk through the examples we've got...

## Minimal registration

This is the minimal set of metadata required to define an IGSN - the `registrant` field pointing to the allocating agent, and the identifier itself. Not very useful but easy to do:

```yaml
"@context": http://schema.igsn.org/json/registration/v0.1/context.jsonld
igsn:
  kind: igsn
  id: XXXCSIRO0001
registrant:
  name: CSIRO
  identifiers:
    - kind: orcid
      id: 0001-0001-0001-0001
    - kind: viaf
      id: https://csiro.au/path/to/viaf.file
    - kind: uri
      id: https://csiro.au
```

You can see a version with extra comments for all the fields here: [minimal_registraion.yaml](https://github.com/IGSN/igsn_json/blob/master/examples/minimal_registration.yaml), and a JSON transpilation here [minimal_registration.json](https://github.com/IGSN/igsn_json/blob/master/examples/minimal_registration.json) (which is how it would come off the server).

## Full registration - extra registration metadata

Obviously an identifier by itself isn't very useful - we want to be able to add extra information which will allow us to link this sample to descriptive information and to other samples and entities.

There is an annotated YAML document for this example here: [full_registration.yaml](https://github.com/IGSN/igsn_json/blob/master/examples/full_registration.yaml) and in JSON: [full_registration.json](https://github.com/IGSN/igsn_json/blob/master/examples/full_registration.json)

### Extra registration fields

There are three other fields that you can add: related resources (with the `related` property), the sample log (under the `log` property) and descriptive metadata (under the `description` property). We'll leave the desciptive metadata for a moment and cover off on the first two properties.

THe related items contains links to other identifiers (including other IGSNs) which are related to this object.

```yaml
related:
  -
    identifier:
      id: https://igsn.org/XXXCSIRO0002
      kind: igsn
    relationshipType: "relatedTo"
  - 
    identifier:
      id: https://igsn.org/XXXCSIROCOLL001
      kind: igsn
    relationship: "childOf"
  - 
    identifier:
      id: https://csiro.au/sampleDocs/XXCSIRO0001
      kind: uri
    relationship: "documentedBy"
```

The `relationshipType` field is controlled in an enumeration in the [`relatedIdentifier.schema.json` document](https://github.com/IGSN/igsn_json/blob/master/schema.igsn.org/json/registration/v0.1/relatedIdentifier.schema.json#L11). This is pretty minimal at this stage and needs to be expanded with our communities' help.

The log contains information about changes to the sample metadata:

```yaml
log:
  - 
    eventType: submitted
    timestamp: 2020-04-13 11:33:04
    comment: Initial submission by Jess to CSIRO
  - 
    eventType: registered
    timestamp: 2020-05-21 14:32:58
    comment: Sample registered by CSIRO with IGSN
  - 
    eventType: updated
    timestamp: 2020-05-21 14:33:45
    comment: Sample description updated by Jess
```

Here we show when the sample was submitted, when it was registered with the central IGSN registry, and then when I updated the descriptive metadata. The eventTypes are controlled with an enumeration in the [`core.schema.json` JSONSchema document](https://github.com/IGSN/igsn_json/blob/master/schema.igsn.org/json/registration/v0.1/core.schema.json#L14) 

## Descriptive metadata

IGSN metadata is split into registration (or core) metadata, which is very minimal, and descriptive (or community) metadata, which containst all the actual 'information' about a sample such as scientific observations, sampling locations etc.

## The lifecycle of a sample

To show how all these parts fit together to give rich sample metadata across organizations, we'll make up a little story about a tooth discovered in Lake Mungo in Australia (acutally this is pretty close to real science but told from a non-expert point of view).


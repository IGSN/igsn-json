# Example IGSN metadata documents

These are examples of simple JSON documents to give you an intuitive feel for how they should be structured.

> **Disclaimer:** This is a proposal at this stage and as such is designed ot be a strawman to start discussion. If you don't like something here then please raise it in the [discussion board](https://github.com/orgs/IGSN/teams/igsn-2040-sprint). I also haven't tested the descriptive metadata against all the schemas (in fact we don't have one for that yet) so there may be elements that aren't 100% correct. Be nice!

We provide the examples in YAML so that they're easier to read (and because JSON doesn't support comments), but you can convert these to JSON with the Python script pretty easily:

```bash
$ python convert.py minimal_registration.yaml
{
    "@context": "https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/registration/v0.1/context.jsonld",
    "igsn": "XXXCSIRO0001",
    "registrant": {
        "name": "CSIRO",
        "identifiers": [
            {
                "kind": "orcid",
                "id": "0001-0001-0001-0001"
            },
            # and so on...
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
"@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/registration/v0.1/context.jsonld
"@id": https://csiro.au/bogus_igsns/XXXCSIRO0001
igsn: XXXCSIRO0001
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

You can see a version with extra comments for all the fields here: [minimal_registraion.yaml](https://github.com/IGSN/igsn-json/blob/master/examples/minimal_registration.yaml), and a JSON transpilation here [minimal_registration.json](https://github.com/IGSN/igsn-json/blob/master/examples/minimal_registration.json) (which is how it would come off the server).

## Full registration - extra registration metadata

Obviously an identifier by itself isn't very useful - we want to be able to add extra information which will allow us to link this sample to descriptive information and to other samples and entities.

There is an annotated YAML document for this example here: [full_registration.yaml](https://github.com/IGSN/igsn-json/blob/master/examples/full_registration.yaml) and in JSON: [full_registration.json](https://github.com/IGSN/igsn-json/blob/master/examples/full_registration.json)

### Extra registration fields

There are three other fields that you can add: related resources (with the `related` property), the sample log (under the `log` property) and descriptive metadata (under the `description` property). We'll leave the desciptive metadata for a moment and cover off on the first two properties.

THe related items contains links to other identifiers (including other IGSNs) which are related to this object.

```yaml
related:
  - identifier:
      id: https://igsn.org/XXXCSIRO0002
      kind: igsn
    relationshipType: "relatedTo"
  - identifier:
      id: https://igsn.org/XXXCSIROCOLL001
      kind: igsn
    relationship: "childOf"
  - identifier:
      id: https://csiro.au/sampleDocs/XXCSIRO0001
      kind: uri
    relationship: "documentedBy"
```

The `relationshipType` field is controlled in an enumeration in the [`relatedIdentifier.schema.json` document](https://github.com/IGSN/igsn-json/blob/master/schema.igsn.org/json/registration/v0.1/relatedIdentifier.schema.json#L11). This is pretty minimal at this stage and needs to be expanded with our communities' help.

The log contains information about changes to the sample metadata:

```yaml
log:
  - eventType: submitted
    timestamp: 2020-04-13 11:33:04
    comment: Initial submission by Jess to CSIRO
  - eventType: registered
    timestamp: 2020-05-21 14:32:58
    comment: Sample registered by CSIRO with IGSN
  - eventType: updated
    timestamp: 2020-05-21 14:33:45
    comment: Sample description updated by Jess
```

Here we show when the sample was submitted, when it was registered with the central IGSN registry, and then when I updated the descriptive metadata. The eventTypes are controlled with an enumeration in the [`main.schema.json` JSONSchema document](https://github.com/IGSN/igsn-json/blob/master/schema.igsn.org/json/registration/v0.1/main.schema.json#L14)

## Descriptive metadata

IGSN metadata is split into registration (or core) metadata, which is very minimal, and descriptive (or community) metadata, which containst all the actual 'information' about a sample such as scientific observations, sampling locations etc.

Why do we seperate descriptive metadata from the core registration metadata? The reason is that IGSN needs to serve a range of scientific and technical communities. Things that you might consider essential features of a sample (e.g. the original latitude and longitude of your rock for a geologist) may not be as useful or completely undefined for another field (e.g. a sample of a comet from a space mission). Core registration metadata is required for all samples from all communities and the more we stuff that core metadata schema the more difficult IGSN becomes to use in a cross-domain way.

Our solution is to allow communities to define and use their own JSONSchema and JSON-LD context documents. The idea is that communities know their own data intimately and understand how intent shapes what informatoin is essntial and what is less central. IGSN eV _may_ have a role in publishing or helping to highlight community documents (this hasn't been decided yet).

In the `full_registration` example we show how you can combine multiple JSON-LD contexts to construct a semantically enabled description. Once that context file is created it becomes very easy to teamplate new samples and information using this same JSON-LD context.

```yaml
description:
  "@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/observations/v0.1/sosa_context.jsonld
  sampleType: "rock"
  collector: Jess Robertson
  curator: Doug Fils
  samplingLocation:
    "@context": https://geojson.org/geojson-ld/geojson-context.jsonld
    geometry:
      type: MultiPoint
      coordinates: [[0, 1], [2, 3], [4, 5], [-3, -2]]
  observations:
    - featureOfInterest: rockiness
      madeBySensor: Jess
      usedProcedure: looked at it
      hasSimpleResult: rock level 9000
      resultTime: 2020-05-21 15:06:47
    - featureOfInterest: taste
      madeBySensor: Jess
      usedProcedure: engage rocklicker
      hasSimpleResult: tastes like chicken
      resultTime: 2020-05-21 15:10:19
```

Here we've used a combination of SOSA tags, with GeoJSON for the location information. We're making use of JSON-LD's nested contexts to provide subcontexts for elements of the document which have different definitions.

This lets us use different meanings for the `coordinates` property in the `observations` and the `sampleLocation`. Why might you want to do this? One example could be taking mass spec spots at coordinates on a sample slide, while the coordinates in the sampling location for the slide might point to a latitude/longitude point on the Earth's surface. By using different contexts we avoid a nasty explosion of global names like `massSpectrometerSlideCoordinates` and `rockSampleLocationCoordinates` which hurt developers down the track without sacrificing interoperability.

## The lifecycle of a sample

To show how all these parts fit together to give rich sample metadata across organizations, we'll make up a little story about a wombat tooth discovered in Lake Mungo in Australia (acutally this is pretty close to real science but told from a non-expert point of view).

### Step 1: specimen and sample collection

We'll say that an archeology team from ANU, in collaboration with the Museum of Fictional Objects (MFO) has gone out and collected their tooth. They've registered the tooth as a sample/specimen with IGSN, including a basic description of the sample, links to other things like photographs, and some information about where the sample is located within the MFO:

```yaml
"@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/registration/v0.1/context.jsonld
igsn: XXXMFO0001
registrant:
  name: Museum of Fictional Objects
  identifiers:
    - kind: uri
      id: https://mfo.org
    - kind: orcid
      id: 9999-9999-9999-9999
description:
  "@context": http://schema.mfo.org/specimens/context.jsonld
  sampleDescription: >
    An interesting tooth collected from Lake Mungo in Australia
    by the ANU archeology team.

  stratigraphicLocation:
    kind: igsn
    id: XXXMFO0002
    relationship: conformal

  photograph: http://photos.mfo.org/lake_mungo_tooth.png

  mfoId: 508.93
  mfoLocation: Stack 4, part b

log:
  - eventType: submitted
    timestamp: 2020-05-22 06:41:04
    comment: Initial submission from the field by archeology team
  - eventType: registered
    timestamp: 2020-05-22 06:41:32
    comment: Sample registered by MFO with IGSN
```

The team have also sampled the stratigraphic horizon that this tooth was found in, and created an IGSN for this sample too:

```yaml
"@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/registration/v0.1/context.jsonld
igsn: XXXMFO0002
registrant:
  $ref: http://igsn.org/XXXMFO001#registrant
description:
  "@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/description/geosamples/v0.1/context.jsonld
  description: A sample of 'A' horizon in Lake Mungo, Australia
  sampleType: sediment
  collector: ANU archeology team
  curator: Early Australia branch, MFO
  isSampleOf:
    kind: uri
    id: https://ga.gov.au/waterbodies/lake_mungo
  samplingLocation:
    "@context": https://geojson.org/geojson-ld/geojson-context.jsonld
    geometry:
      type: Point
      coordinates: [143.055385, -33.715259]
log:
  - eventType: submitted
    timestamp: 2020-05-22 06:41:04
    comment: Initial submission from the field by archeology team
  - eventType: registered
    timestamp: 2020-05-22 06:41:32
    comment: Sample registered by MFO with IGSN
```

Again, they've included references to the thing that the sample is supposed to be representative of (in this case a stratigraphic horizon via an identifier managed by the federal geological survey Geoscience Australia), and the location that the sample comes from, given in GeoJSON format.

Then we can link the two samples by including a link to `XXXMFO0002` in the related identifiers property for `XXXMFO0001`:

```yaml
# snip other stuff for XXXMFO0001
related:
  - identifier:
      id: https://igsn.org/XXXMFO002
      kind: igsn
    relationshipType: isPartOf
```

> Note, to save space we're just showing the properties which are added as we go. You ou can see all the data for this step in [lifecycle_1.yaml](https://github.com/IGSN/igsn-json/blob/master/examples/lifecycle_1.yaml).
>
> We're also combining several YAML files into a single one for this example for clarity. These would normally be seperate docuements/resources on the server. If you use the `convert.py` script to convert these to JSON it will glom them all into an array. For example here we pull the IGSN out of each document:
>
> ```bash
> $ python convert.py lifecycle_3.yaml | jq '.[].igsn.id'
> "XXXMFO0001"
> "XXXMFO0002"
> "XXXCSIRO001"
> ```

### Step 2: Sample dating

Back at ANU the team does some radiocarbon dating on their soil horizon sample. They get an age of 40 ka, and update the soil horizon descriptive metadata to reflect this:

```yaml
# in XXXMFO0002
description:
  observations:
    - featureOfInterest: age
      madeBySensor: mass spectrometer
      usedProcedure: carbon date
      hasResult:
        units: ka
        value: 40
      resultTime: 2020-05-22 06:49:48
log:
  - eventType: updated
    timestamp: 2020-05-22 07:06:32
    comment: Sample dated
```

Because they intended this soil sample to be dated in relation to the tooth, they also update the metadata for the tooth sample, in a way that makes sense for a tooth specimen:

```yaml
# in XXXMFO0001
description:
  age: 40000 years
  datingMethod: stratigraphic carbon
  datingSample:
    kind: igsn
    id: XXXMFO0002
log:
  - eventType: updated
    timestamp: 2020-05-22 07:43:12
    comment: Date updated from stratigraphic sample
```

> The full example for this step is in [lifecycle_2.yaml](https://github.com/IGSN/igsn-json/blob/master/examples/lifecycle_2.yaml)

### Step 3: Subsampling and chemical analysis

Now that they know the age of the animal tooth, the team decides they'd like to find out something about the animal's range by doing some isotopic analysis. They engage CSIRO (who have an overabundance of mass specs) to do this work. The CSIRO lab team take a small sample, and register this as a new sample with IGSN:

```yaml
"@context": https://raw.githubusercontent.com/IGSN/igsn-json/master/schema.igsn.org/json/registration/v0.1/context.jsonld
igsn: XXXCSIRO001
registrant:
  name: Commonwealth Scientific and Industrial Research Organization
  identifiers:
    - kind: uri
      id: https://csiro.au
related:
  - identifier:
      kind: igsn
      id: XXXMFO0001
    relationshipType: isParent
description:
  "@context": http://schema.csiro.au/labsamples/context.jsonld
  sampleOwner:
    kind: orcid
    id: 9999-9999-9999-9999
  request: Sr/Nd ratios
  parentSample: https://igsn.org/XXXMFO001
log:
  - eventType: submitted
    timestamp: 2020-05-22 07:45:11
  - eventType: registered
    timestamp: 2020-05-22 07:45:22
```

They then do the analysis:

```yaml
# XXXCSIRO001
description:
  # ...
  observations:
    - featureOfInterest: composition
      madeBySensor: mass spectrometer
      hasResult:
        Sr:
          units: partsPerMillion
          value: 40
          variance: 13
        Nd:
          units: partsPerBillion
          value: 8
          variance: 5
        Ca:
          units: percent
          value: 10
          variance: 2
    - featureOfInterest: density
      madeBySensor: scales
      hasResult:
        units: gramsPerCubicCentimetre
        value: 10
log:
  - eventType: destroyed
    timestamp: 2020-05-22 07:45:38
    comment: This sample has been destroyed in testing
  - eventType: updated
    timestamp: 2020-05-22 14:54:07
    comment: Updated with measurement info
```

Because the sample is destroyed by the laser, they update the metadata to indicate that this sample has been destroyed.

CSIRO sends the information back to the ANU/MFO team, along with the IGSN info about the sample they used. The team updates their records to include the measurements they care about:

```yaml
# XXXMFO0001
related:
  - identifier:
      id: https://igsn.org/XXXCSIRO001
      kind: igsn
    relationshipType: isChild
description:
  composition:
    Sr:
      units: partsPerMillion
      value: 40
    Nd:
      units: partsPerBillion
      value: 8
    Ca:
      units: percent
      value: 10
  compositionSample:
    kind: igsn
    id: http://igsn.org/XXXCSIRO01
log:
  - eventType: updated
    timestamp: 2020-05-22 07:44:39
    comment: Composition added from CSIRO
```

Based on this new data they go out and write an award-winning paper that revolutionises our understanding of animal ranges 40,000 years ago in south-eastern Australia, referencing all their samples using IGSN PIDS of course!

> The full example for this step is in [lifecycle_3.yaml](https://github.com/IGSN/igsn-json/blob/master/examples/lifecycle_3.yaml)

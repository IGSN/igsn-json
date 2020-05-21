# IGSN JSON development for the IGSN 2040 Sprint 1 (May/June 2020)

Welcome to the test schema repo for the IGSN 2040 Architecture Sprint!

Here's a list of important things in this repository to get you going quickly:

- _Example metadata documents_ - you can see some examples (in YAML with annotations, and in JSON) in [this folder here](https://github.com/IGSN/igsn_json/blob/master/examples/examples.md)
- _JSONSchema and JSON-LD documents_ If you want to validate your JSON documents against a schema then you can [find them here for registration metadata](https://github.com/IGSN/igsn_json/tree/master/schema.igsn.org/json/registration/v0.1). We also have some demo 'community schemas' for [descriptive metadata here](https://github.com/IGSN/igsn_json/tree/master/schema.igsn.org/json/description)
- _More info on this sprint_: head to the [wall of text below](https://github.com/IGSN/igsn_json#context)
- _Want to see the work in progress?_: head to [the issue board](https://github.com/IGSN/igsn_json/issues) to see what's happening or contribute.
- _Original IGSN docs_: [these have a lot of info](https://igsn.github.io/) on IGSN metadata, justifications for the core fields etc.

Otherwise feel free to dive in and get your hands dirty. We're all making it up as we go along so don't feel like you've got to know what you're saying before asking a question.

## Developing schemas and JSON-LD contexts

We're going to build out the shared schemas and contexts in this repo - all of the references in the schema are to the raw versions of these documents on the master branch of this repo.

So if you want to add new terms etc, then open an issue and we can work on a pull request. If you're not sure about the code side then just open an issue in this repo and we'll find some people that know what to do to help you out.

## Meeting schedule

We're planning on having a few video-to-video meetings over the course of the sprint. Please email [XXX](firstname.lastname@example.com) for the meeting links.

As we're spread all around the world getting a time that suits everyone is a bit challenging. If you can't make these we will post recordings of these here:

| Date   | Time (UTC) | Recorded video link |
| ------ | ---------- | ------------------- |
| Monday | XXXX       | TBC                 |
| Monday | XXXX       | TBC                 |
| Friday | XXXX       | TBC                 |

## Getting help

If something's not clear, raise an issue in the [issue tracker](https://github.com/IGSN/igsn_json/issues).

If you're not sure where something goes or you'd rather talk to a human than Octocat then please get in touch with one of these lovely people: Jens Klump (in Perth/Oceania time zones, [jens.klump@csiro.au](mailto:jens.klump@csiro.au), Doug Fils (in central US timezones, [drfils@gmail.com](mailto:drfils@gmail.com)) or XX (in European timezones, [firstname.lastname@host.com](firstname.lastname@host.com))

## Context

The current implementation of IGSN is an excellent combination of lean centralised functions that are supported by federated services. This has given IGSN the ability to adapt to requirements arising from new communities joining the system. To accommodate a more diverse community of users and a much larger number of sample registrations requires a number of changes.

In particular, there are two new roles within the IGSN architecture – that of an allocating agent, who publishes data in a minimal and cost-effective way, and the data aggregators who provide services that consume and republish that data in more powerful ways (but which potentially come with higher support and service costs). Both of these roles are currently carried out by allocating agents, but by forcing agents to also provide aggregated data services raises the resources required to become an agent and makes the role less sustainable in the longer term.

Under the new scheme, we propose that agents simply publish JSON documents on their landing pages which aggregators can crawl to uncover new data, along with a sitemap pointing to all the landing pages which contain sample data. Agents would not be responsible for providing high-frequency or high-volume query support against this data – that would be the role of the aggregator. Aggregators would have a responsibility to their end-users to provide services that are performant and scientifically useful, removing this burden from the agents.
For the relationship between agents and aggregators to work effectively, we need to outline the contract governing the relationship. In the long run, we want these roles to be as decoupled as possible, but while we are developing recommendations it would be good to have both in the room to ensure that we are balancing the needs of the two roles effectively.

In this sprint we want to test and evaluate the implementation of sharing and aggregating IGSN metadata between IGSN Agents and Metadata Aggregators.

### Aims of the sprint

- Determine how difficult (or not) it will be for agents to make the required changes to their landing pages to conform to the new requirements and provide crawler guidance in robot.txt and sitemap.xml files.
- Determine how difficult or not it is will be to develop new web crawlers for aggregators to aggregate data.
- Uncover any new ways of using aggregated data that might be of interest to the community
- Determine what services IGSN eV needs to provide to agents to support their publication role (e.g. publication of JSON Schema, JSON LD contexts etc, authentication, role-based access etc)

## Developing schemas and running tests

We're using some lightweight checks with pytest as a testing harness. Take a look at the python files in the [tests](https://github.com/IGSN/igsn_json/tree/master/tests) folder for how these work. Basically we just fire a bunch of JSON fragments that should validate against our schemas. This has the bonus of checking that all our JSON references etc are correct.

We're using [pipenv](https://pipenv.pypa.io/en/latest/) to manage the Python environment and dependencies. To install pipenv just do

```bash
pip install pipenv
```

and then you can install the environment with

```bash
pipenv install --dev
```

Pipenv creates an isolated environment for you - you will need to run pytest inside of this. To do this, just do

```bash
$ cd /path/to/igsn_json
$ pipenv run python -m pytest
================================== test session starts ===================================
platform win32 -- Python 3.7.5, pytest-5.4.2, py-1.8.1, pluggy-0.13.1 -- c:\users\jesse\.virtualenvs\igsn_json-uu6qpojl\scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\jesse\OneDrive\Documents\IGSN\igsn_json, inifile: setup.cfg
collected 10 items

tests/test_registration_schema.py::test_igsn_registration[obj0-True] PASSED         [ 10%]
tests/test_registration_schema.py::test_igsn_registration[obj1-False] PASSED        [ 20%]
tests/test_registration_schema.py::test_igsn_registration[obj2-False] PASSED        [ 30%]
tests/test_registration_schema.py::test_igsn_registration[obj3-False] PASSED        [ 40%]
tests/test_registration_schema.py::test_igsn_registration[obj4-True] PASSED         [ 50%]
tests/test_registration_schema.py::test_igsn_registration[obj5-True] PASSED         [ 60%]
tests/test_registration_schema.py::test_igsn_registration[obj6-True] PASSED         [ 70%]
tests/test_registration_schema.py::test_igsn_registration[obj7-False] PASSED        [ 80%]
tests/test_registration_schema.py::test_igsn_registration[obj8-True] PASSED         [ 90%]
tests/test_registration_schema.py::test_igsn_registration[obj9-True] PASSED         [100%]

- generated xml file: C:\Users\jesse\OneDrive\Documents\IGSN\igsn_json\tests\reports\test-output.junit.xml -
=================================== 10 passed in 1.30s ===================================

```

in the root folder of the repository.

We're also using [Travis](xx) (need to update the Travis link once public) to automatically check pull requests, so you may get asked to clean things up if your tests are failing before we can merge your contribution. If you've got any questions about this just ping [@jesserobertson](https://github.com/jesserobertson).

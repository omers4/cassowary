# cassowary

[![Build Status](https://travis-ci.org/omers4/cassowary.svg?branch=master)](https://travis-ci.org/omers4/cassowary)
[![codecov](https://codecov.io/gh/omers4/omers-final-project/branch/master/graph/badge.svg)](https://codecov.io/gh/omers4/omers-final-project)
[![Documentation Status](https://readthedocs.org/projects/omers-final-project/badge/?version=latest)](https://omers-final-project.readthedocs.io/en/latest/?)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:omers4/cassowary.git
    ...
    $ cd cassowary/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [cassowary] $
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `cassowary` package also provide a command-line interface:

The CLI provides the following commands:

`run` command, for running the server and start listening for thoughts:

```sh
$ python -m run ADDRESS DATA_DIR
```

`upload` command, for uploading a thought to the server:

```sh
$ python -m upload ADDRESS USER THOUGHT
done
```

`run-web-server` command, for starting the web server

```sh
$ python -m run-web-server ADDRESS DATA_DIR
```

## The HTTP API

`GET /users`
Returns the list of all the supported users, including their IDs and names only.

`GET /users/user-id`
Returns the specified user's details: ID, name, birthday and gender.

`GET /users/user-id/snapshots`
Returns the list of the specified user's snapshot IDs and datetimes only.|

`GET /users/user-id/snapshots/snapshot-id`
Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose).

`GET /users/user-id/snapshots/snapshot-id/result-name`
Returns the specified snapshot's result in a reasonable format.


### How to add a new parser

1. Add a new module called `yourname_parser.py` inside `parsers` package
2. Inside yourname_parser.py, add a new class decorated with `@parser` and inherits BaseParser, for example:
```@parser('pose')
class PoseParser(BaseParser):
    def parse(self, data):
        return {}
```
3. Implement the parser to return your result in `parse` method.
4. Test your parser, running `python -m cassowary.parsers parse myparser <json data>`
5. You're good to go!
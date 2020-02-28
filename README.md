# cassowary

[![Build Status](https://travis-ci.org/omers4/cassowary.svg?branch=master)](https://travis-ci.org/omers4/cassowary)
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

## Run everything together
requirements: docker, root access.
run the following script as root:
```sh
./scripts/run-pipelines.sh
```
Once the script is done, you can:
1. go to http://localhost:8080 to see the gui
2. Call the http API, running on http://localhost:8888 (more on HTTP API later)
3. run ```python -m cassowary.cli get-users -p 8888``` to run the cli commands (more on CLI commands later)


## Usage
The `cassowary` package can function as a python library, and also provides a command-line interface.
### Use from command line
the format is
```sh
python -m cassowary.<part> <command> [ARGUMENTS] [OPTIONS]
```

### Use as python library
after activating the virtual environment, you can run:
```python
from cassowary.<part> import <command>
```

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
5. Add your parser to the run-pipelines.sh script in the following format: 
6. You're good to go!

# The components

## The client - Upload a snapshot
The client simply parses the snapshots from a given file and connects to the server, then sending the snapshots to the server.
From command line:
```sh
python -m cassowary.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
```

From python:
```python
>>> from cassowary.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz', reader=ProtobuffReader)
```
The client CLI currently reads only protobuffs, but its easy to give another reader when using Python, by just giving a differen reader (like ```BinaryReader```). the reader should inherit ```BaseReader```. 

## The server
The server listents to connections from clients, in order to receive snapshots and pass them to the queue.
The binary data is written to ```/parsed_results/```.
The server is implemented with simple python threading & sockets.

From command line:
```sh
python3 -m cassowary.server run-server PUBLISH_URL -h HOST -p PORT
```

From python:
```python
>>> from cassowary.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.01', port=8000, publish=print_message)
```


## The HTTP API
The http API is implemented using Flask.

From command line:
```sh
python3 -m cassowary.api run-server -h HOST -p PORT -d DATABASE_URL
```
From Python:
```sh
>>> from cassowary.api import run_api_server
>>> run_api_server(
...     host = '127.0.0.1',
...     port = 5000,
...     database_url = 'mongodb://127.0.0.1:27017',
... )
```

After the server is up, you can start sending http requests to host:port:

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


# omers-final-project

[![Build Status](https://travis-ci.org/omers4/omers-final-project.svg?branch=master)](https://travis-ci.org/omers4/omers-final-project)
[![codecov](https://codecov.io/gh/omers4/omers-final-project/branch/master/graph/badge.svg)](https://codecov.io/gh/omers4/omers-final-project)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:advanced-system-design/omers-final-project.git
    ...
    $ cd omers-final-project/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [omers final project] $
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `omers-final-project` package also provide a command-line interface:

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
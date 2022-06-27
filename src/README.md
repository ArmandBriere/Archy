
# Cloud Functions

## Run locally

```bash 
# pwd = functions/exp
functions-framework --target exp
```

Then you can POST to the correct URL

```bash
curl -m 70 -X POST localhost:8080/exp -H "Authorization:bearer $(gcloud auth print-identity-token)" \
-H "Content-Type:application/json" \
-d '{"name": "tmp"}'
```

Call a local function

```bash
curl -H "Authorization: bearer $(./google-cloud-sdk/bin/gcloud auth print-identity-token)" https://us-central1-archy-f06ed.cloudfunctions.net/archy_py
```

# Testing & lint

[Tox](https://tox.wiki/en/latest/) is used to automate testing.

Simply run the `tox` command to execute all the test script in the `tox.ini` file.

- `pytest` -> Unit test framework.
- `black` -> Code formatter.
- `pylint` -> Static code analysis tool for lint.
- `isort` -> isort your imports, so you don't have to.

You can run the script by hand if you want:

```bash
python -m pytest --rootdir .
black -l 120 .
pylint functions tests main.py
isort .
```

## Requirements

- `pytest` -> Framework use to run the tests
- `MagicMock` -> Mock from the `unnitest` library (documentation)[https://docs.python.org/3/library/unittest.mock.html]

## How to write test

We are writting tests for the serverless cloud functions. Those are http endpoint that expect a `request` as input:

```py
import functions_framework
from typing import Tuple


@functions_framework.http
def hello(request) -> Tuple[str, int]:
    """HTTP Cloud Function."""

    request_json: Optional[Any] = request.get_json(silent=True)
    return "Hello world!", 200
```

With google cloud function, the request is a [Flask Request](https://tedboy.github.io/flask/generated/generated/flask.Request.html)

An easy solution to test thoses functions is to use a mock of the request object.

## Mock

A mock objects is a simulated object that mimic the behavior of real objects (wikipedia)[https://en.wikipedia.org/wiki/Mock_object]

The idea is to create a new `Mock` object instead of a `Flask Request` and to override the `return_value`. Like this, we control that the `get_json` will return the desired `body`

This is how we do it:

1. Import `MagicMock`

```py
from unittest.mock import MagicMock
```

2. Create a `MagicMock` instance. Remember to properly name your variable.

```py
request_mock = MagicMock()
```

3. Override the `return_value` of the `get_json`

```py
request_mock.get_json.return_value = {"name": "Paul"}
```

4. Pass the mock object as an input of the function we want to test

```py
hello(request_mock)
```

Full test example

```py
from unittest.mock import MagicMock

from functions.hello.main import hello


def test_hello():
    body = {"name": "Paul"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert ("Hello world!", 200) == result
```

## How to run test

The tests can be run in the command line or with VsCode.

The python path is defined in the `pytest.ini` file, run this command to run the tests:

```bash
pytest
```

In VsCode, open a test file and select the testing menu on the sidenav.

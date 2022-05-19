# tox

Tox is used to automate testing

Simply run the `tox` command to execute all the test script in the `tox.ini` file

- `pytest` -> Unit test framework
- `black` -> Code formatter
- `pylint` -> Static code analysis tool for lint
- `isort` -> isort your imports, so you don't have to.

You can run the script by hand if you want

```bash
python -m pytest --rootdir .
black -l 120 .
pylint functions tests main.py
isort .
```
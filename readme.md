# Archy discord bot

## Ressources

[Discord python documentation](https://discordpy.readthedocs.io/en/stable/index.html)

## Google cloud cli

Install the [Google Cloud Cli](https://cloud.google.com/sdk/docs/install)

## Functions

The code is deployed as [functions](https://cloud.google.com/sdk/gcloud/reference/functions) on Google Cloud

- [Code samples](https://cloud.google.com/functions/docs/samples?hl=fr)

[Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python)

### Run locally

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

### Deploy

```bash
gcloud functions deploy FUNCTION_NAME --runtime=python38 --entry-point=hello --trigger-http
```

### Call

```bash
curl -H "Authorization: bearer $(./google-cloud-sdk/bin/gcloud auth print-identity-token)" https://us-central1-archy-f06ed.cloudfunctions.net/archy_py
```

## Google Compute Engine VM instance

- SSH command, we should not use that

```bash
gcloud compute ssh --zone "us-central1-a" "e2-micro-archy"  --project "archy-f06ed"
```

### Deployement

```bash
docker build -t us.gcr.io/archy-f06ed/archy .
docker push us.gcr.io/archy-f06ed/archy
gcloud compute instances update-container e2-micro-archy
```

## tox

Tox is used to automate testing

Simply run the `tox` command to execute all the test script in the `tox.ini` file

- `pytest` -> Unit test framework
- `black` -> Code formatter
- `pylint` -> Static code analysis tool for lint
- `isort` -> isort your imports, so you don't have to.

You can run the script by hand if you want

```bash
pytest
black -l 120 .
pylint functions tests main.py
isort .
```

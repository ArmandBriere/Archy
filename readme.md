# Archy discord bot

## Ressources

[Discord python documentation](https://discordpy.readthedocs.io/en/stable/index.html)

## Google cloud cli

Install the [Google Cloud Cli](https://cloud.google.com/sdk/docs/install)

## Functions

The code is deployed as [functions](https://cloud.google.com/sdk/gcloud/reference/functions) on Google Cloud

- [Code samples](https://cloud.google.com/functions/docs/samples?hl=fr)

[Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python)

### Deploy

```bash
gcloud functions deploy my_function --runtime=python37
```

### Call

```bash
curl -H "Authorization: bearer $(./google-cloud-sdk/bin/gcloud auth print-identity-token)" https://us-central1-archy-f06ed.cloudfunctions.net/archy_py
```

## Google cloud discord bot

This doc explains how we can create a simple [vm instance](https://cloud.google.com/blog/topics/developers-practitioners/build-and-run-discord-bot-top-google-cloud)

## Google Compute Engine VM instance

- SSH command

```bash
gcloud compute ssh --zone "us-central1-a" "instance-1"  --project "archy-f06ed"
```

## Enable container registry

```bash
gcloud services enable containerregistry.googleapis.com
```

To authenticate your request, follow the steps in: https://cloud.google.com/container-registry/docs/advanced-authentication


## Deployement

```bash
docker build -t us.gcr.io/archy-f06ed/archy .
docker push us.gcr.io/archy-f06ed/archy
gcloud compute instances update-container instance-1
```
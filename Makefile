default:

prod: build push
dev: build-dev push-dev

build:
	docker build -t us.gcr.io/archy-f06ed/archy-prod -f Dockerfile.prod .

push:
	docker push us.gcr.io/archy-f06ed/archy-prod

build-dev:
	docker build -t us.gcr.io/archy-f06ed/archy-dev -f Dockerfile.dev .

push-dev:
	docker push us.gcr.io/archy-f06ed/archy-dev

restart:
	gcloud compute instances update-container e2-micro-archy


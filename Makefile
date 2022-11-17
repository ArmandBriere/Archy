default:

prod: build push restart
dev: build-dev push-dev restart

build:
	docker build -t us.gcr.io/archy-f06ed/archy Dockerfile.prod

push:
	docker push us.gcr.io/archy-f06ed/archy

build-dev:
	docker build -t us.gcr.io/archy-f06ed/archy-dev Dockerfile.dev

push-dev:
	docker push us.gcr.io/archy-f06ed/archy-dev

restart:
	gcloud compute instances update-container e2-micro-archy


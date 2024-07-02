default:

prod: build push
dev: build-dev push-dev

build:
	docker build -t northamerica-northeast1-docker.pkg.dev/archy-f06ed/archy/archy-prod -f Dockerfile.prod .

push:
	docker push northamerica-northeast1-docker.pkg.dev/archy-f06ed/archy/archy-prod

build-dev:
	docker build -t northamerica-northeast1-docker.pkg.dev/archy-f06ed/archy/archy-dev -f Dockerfile.dev .

push-dev:
	docker push northamerica-northeast1-docker.pkg.dev/archy-f06ed/archy/archy-dev

restart:
	gcloud compute instances update-container e2-micro-archy


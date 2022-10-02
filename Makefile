default: build

all: build push restart

build:
	docker build -t us.gcr.io/archy-f06ed/archy .

push:
	docker push us.gcr.io/archy-f06ed/archy

restart:
	gcloud compute instances update-container e2-micro-archy


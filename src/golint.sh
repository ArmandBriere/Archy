#!/bin/sh
find . -name "*.go" -not -path "*/cmd/*.go" -execdir pwd \; -execdir /usr/bin/golangci-lint run --go=1.18 --config=../../.golangci.yml \;

#!/bin/sh
find . -name "*.go" -not -path "*/cmd/*.go" -execdir pwd \; -execdir $(go env GOPATH)/bin/golangci-lint run --go=1.18 \;

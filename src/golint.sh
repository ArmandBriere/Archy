#!/bin/sh
find . -name "*.go" -execdir pwd \; -execdir $(go env GOPATH)/bin/golangci-lint run \;

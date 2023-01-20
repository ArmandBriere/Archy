package main

import (
	"context"

	stm "stm.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	err := stm.CheckStmStatus(context.Background(), stm.PubSubMessage{})
	if err != nil {
		panic(nil)
	}
}

package main

import (
	"log"
	"os"

	_ "pm.com/cloudfunction"

	"github.com/GoogleCloudPlatform/functions-framework-go/funcframework"
)

func main() {
	// Use PORT environment variable, or default to 8080.
	port := "8080"
	if envPort := os.Getenv("PORT"); envPort != "" {
		port = envPort
	}

	if err := funcframework.Start(port); err != nil {
		log.Fatalf("framework.Start: %v\n", err)
	}
}

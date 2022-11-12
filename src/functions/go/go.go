package _go

import (
	"fmt"
	"net/http"
)

// Send a message and react on it
// This is a template function that show discord interaction
func Go(w http.ResponseWriter, r *http.Request) {
	// Parse body to get Payload
	fmt.Fprint(w, "Golang is faster!")
}

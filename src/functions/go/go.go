package _go

import (
	"fmt"
	"net/http"
)

// Go template function
func SendMessage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Golang is faster!")
}
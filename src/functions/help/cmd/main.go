package main

import (
	"net/http"
	"net/http/httptest"

	help "help.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	w := httptest.NewRecorder()

	help.GetHelp(w, req)
}

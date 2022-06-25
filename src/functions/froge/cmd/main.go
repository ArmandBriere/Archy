package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	froge "froge.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	body := []byte(`{"channel_id": "<CHANNEL_ID>", "server_id" : "<SERVER_ID>"}`)

	reader := bytes.NewReader(body)
	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	froge.SendRandomFroge(w, req)
}

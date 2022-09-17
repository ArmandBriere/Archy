package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	warn "warn.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	body := []byte(`{
		"server_id": "123",
		"user_id": "123",
		"channel_id": "123",
		"mentions": ["123"],
		"message": "hi"}
	`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	warn.WarnUser(w, req)
}

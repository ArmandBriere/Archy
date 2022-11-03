package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	levelFaster "levelFaster.com/cloudfunction"
)

func main() {
	// Add custom channel_id to test
	body := []byte(`{"server_id": "<SERVER_ID>", "user_id": "<USER_ID>"}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	levelFaster.Level(w, req)
}

package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	froge "froge.com/cloudfunction"
)

func main() {
	// Add custom channel_id to test
	body := []byte(`{"channel_id": "<CHANNEL_ID>", "server_id" : "<SERVER_ID>"}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	froge.SendRandomFroge(w, req)
}

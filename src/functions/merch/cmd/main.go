package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	merch "merch.com/cloudfunction"
)

func main() {
	// Add custom channel_id to test
	body := []byte(`{"channel_id": "<CHANNEL_ID>"}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	merch.Merch(w, req)
}

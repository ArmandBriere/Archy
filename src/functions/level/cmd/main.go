package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	levelFaster "level.com/cloudfunction"
)

func main() {
	body := []byte(`{
		"server_id": "<SERVER_ID>", 
		"user_id": "<USER_ID>"
	}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	levelFaster.Level(w, req)
}

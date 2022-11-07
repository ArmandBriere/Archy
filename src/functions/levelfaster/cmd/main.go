package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	levelFaster "levelFaster.com/cloudfunction"
)

func main() {
	body := []byte(`{
		"server_id": "", 
		"user_id": "",
		"mentions": [""]}
	`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	levelFaster.Level(w, req)
}

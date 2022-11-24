package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	levelFaster "level.com/cloudfunction"
)

func main() {
	body := []byte(`{
		"server_id": "964701887540645908", 
		"user_id": "135048445097410560"
	}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	levelFaster.Level(w, req)
}

package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	ban "ban.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	body := []byte(`{"server_id": "<SERVER_ID>", "user_id": "<USER_ID>", "mentions": ["<USER_TO_BAN>"]}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	ban.BanUser(w, req)
}

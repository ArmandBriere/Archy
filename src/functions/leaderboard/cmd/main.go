package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	leaderboard "leaderboard.com/cloudfunction"
)

func main() {
	//Add custom server_id to test
	body := []byte(`{"server_id" : "<SERVER_ID>"}`)

	reader := bytes.NewReader(body)
	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	leaderboard.GetLeaderboardUrl(w, req)
}

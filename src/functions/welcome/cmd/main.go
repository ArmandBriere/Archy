package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"

	welcome "welcome.com/cloudfunction"
)

func main() {
	//Add custom server_id to test
	body := []byte(`{"server_name" : "<SERVER_NAME>"}`,
					`{"user_id" : "<USER_ID>"}`,
					`{"username" : "<USERNAME>"}`,
					`{"avatar_url" : "<AVATAR_URL>"}`,
					`{"channel_id" : "<CHANNEL_ID>"}`)
				)

	reader := bytes.NewReader(body)
	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	welcome.GreetingNewMember(w, req)
}

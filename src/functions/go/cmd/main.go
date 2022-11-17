package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"

	_go "go.com/cloudfunction"
)

func main() {
	// Add custom channel_id to test
	body := []byte(`{}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	_go.SendMessage(w, req)
	fmt.Print(w.Body)
}

package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"

	merch "merch.com/cloudfunction"
)

func main() {
	body := []byte(`{}`)
	reader := bytes.NewReader(body)

	req := httptest.NewRequest(http.MethodGet, "/test", reader)
	w := httptest.NewRecorder()

	// Call function
	merch.Merch(w, req)

	fmt.Print(w.Body)
}

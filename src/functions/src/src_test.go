package src

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSrc(t *testing.T) {
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(Src)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	ok := false
	if rr.Body.String() == srcUrl {
		ok = true
	}
	if !ok {
		t.Errorf("handler returned wrong url")
	}
}

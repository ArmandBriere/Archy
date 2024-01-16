package http

import (
	"encoding/json"
	"fmt"
	"log/slog"
	"net/http"
	"os"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

const (
	httpCatUrl = "https://http.cat/"
)

type Payload struct {
	Params []string `json:"params"`
}

func init() {
	functions.HTTP("Http", Http)
}

func Http(w http.ResponseWriter, r *http.Request) {

	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		slog.Error(fmt.Sprintf("%s: %v", "Cannot parse input payload", err))
		os.Exit(1)
	}

	if len(payload.Params) == 0 {
		fmt.Fprint(w, httpCatUrl+"/418")
		return
	}

	requestedUrl := httpCatUrl + payload.Params[0]

	resp, err := http.Get(requestedUrl)
	if err != nil || resp.StatusCode != 200 {
		fmt.Fprint(w, httpCatUrl+"/404")
		return
	}

	fmt.Fprint(w, requestedUrl)
}

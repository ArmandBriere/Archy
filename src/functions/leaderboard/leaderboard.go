package leaderboard

import (
	"encoding/json"
	"fmt"
	"html"
	"net/http"
	"strings"
)

const baseUrl = "https://archybot.web.app/leaderboard/"

type Payload struct {
	ServerId string `json:"server_id"`
}

func GetLeaderboardUrl(w http.ResponseWriter, r *http.Request) {
	//Parse body to get Payload
	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)

	if err != nil {
		panic(err)
	}

	if len(payload.ServerId) == 0 {
		panic("Missing server id")
	}

	//Build a string efficiently with strings.Builder
	var url strings.Builder
	url.WriteString(baseUrl)
	url.WriteString(payload.ServerId)

	//Send the current server leaderboard url.
	fmt.Fprint(w, html.EscapeString(url.String()))
}

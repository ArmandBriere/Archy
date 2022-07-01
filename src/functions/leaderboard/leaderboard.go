package leaderboard

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"
)

const baseUrl = "https://archybot.web.app/leaderboard/"

type Payload struct {
	ServerId string `json:"server_id"`
}

func SendLeaderboardUrl(w http.ResponseWriter, r *http.Request) string {
	//Parse body to get Payload
	var payload = Payload{}
	json.NewDecoder(r.Body).Decode(&payload)

	if len(payload.ServerId) == 0 {
		log.Print("Missing server id")
		return ""
	}

	//Build a string efficiently with strings.Builder
	var url strings.Builder
	url.WriteString(baseUrl)
	url.WriteString(payload.ServerId)

	//Send the current server leaderboard url.
	return url.String()
}

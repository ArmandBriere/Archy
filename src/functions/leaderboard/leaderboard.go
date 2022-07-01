package leaderboard

import (
	"strings"
	"encoding/json"
	"net/http"
)

const BASE_URL = "https://archybot.web.app/leaderboard/"

var Payload struct {
	ServerId  string `json:"server_id"`
}

func sendLeaderboardUrl(w http.ResponseWriter, r *http.Request){
	//Parse body to get Payload
	var payload = Payload
	json.NewDecoder(r.Body).Decode(&payload)

	//Build a string efficiently with strings.Builder
	var url strings.Builder
	url.WriteString(BASE_URL)
	url.WriteString(payload.ServerId)

	//Send the current server leaderboard url.
	return url.String()
}
package video

import (
	"encoding/json"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"strings"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

const (
	DEFAULT_VIDEO = "<https://www.youtube.com/watch?v=dQw4w9WgXcQ>"
	UNKNOWN_VIDEO = "https://www.youtube.com/watch?v=bnmAi53H520"
	NOT_FOUND_VID = "https://www.youtube.com/watch?v=TSXXi2kvl_0"
)

type YoutubeV3Payload struct {
	Items []struct {
		ID struct {
			Kind    string `json:"kind"`
			VideoID string `json:"videoId"`
		} `json:"id"`
	} `json:"items"`
}

type Payload struct {
	Params []string `json:"params"`
}

// init setup storage and firestore client.
func init() {
	functions.HTTP("Video", Video)
}

// Search youtube videos based on space delimited parameters.
func Video(w http.ResponseWriter, r *http.Request) {
	var payload Payload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		slog.Error(fmt.Sprintf("Error decoding payload: %v", err))
		fmt.Fprintln(w, DEFAULT_VIDEO)
		return
	}

	if len(payload.Params) == 0 || payload.Params[0] == "" {
		slog.Error(fmt.Sprintf("Missing params from main node: %v", err))
		fmt.Fprintln(w, DEFAULT_VIDEO)
		return
	}

	query := strings.Join(payload.Params, "+")
	apiKey := os.Getenv("YOUTUBE_API_KEY")

	res, err := http.Get(fmt.Sprintf(
		"https://www.googleapis.com/youtube/v3/search?key=%s&q=%s&part=snippet&type=video&maxResults=1&safeSearch=strict",
		apiKey,
		query,
	))
	if err != nil || res.StatusCode != 200 {
		slog.Error(fmt.Sprintf("Google Youtube API request failed: %v", err))
		fmt.Fprintln(w, DEFAULT_VIDEO)
		return
	}
	defer res.Body.Close()

	var youtubeResponse YoutubeV3Payload
	err = json.NewDecoder(res.Body).Decode(&youtubeResponse)
	if err != nil || len(youtubeResponse.Items) == 0 {
		fmt.Fprintln(w, NOT_FOUND_VID)
		return
	}

	fmt.Fprintln(w, fmt.Sprintf("https://youtu.be/%s", youtubeResponse.Items[0].ID.VideoID))
}

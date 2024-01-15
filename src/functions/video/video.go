package video

import (
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

const (
	DEFAULT_VIDEO = "<https://www.youtube.com/watch?v=dQw4w9WgXcQ>"
	UNKNOWN_VIDEO = "https://www.youtube.com/watch?v=bnmAi53H520"
	NOT_FOUND_VID = "https://www.youtube.com/watch?v=TSXXi2kvl_0"
)

// init setup storage and firestore client.
func init() {
	functions.HTTP("Video", Video)
}

func Video(w http.ResponseWriter, _ *http.Request) {
}

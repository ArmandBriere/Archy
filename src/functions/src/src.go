package src

import (
	"fmt"
	"log/slog"
	"net/http"
	"os"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
	functions.HTTP("Src", Src)
}

const (
	srcUrl = "https://github.com/ArmandBriere/Archy"
)

func Src(w http.ResponseWriter, r *http.Request) {
	_, err := w.Write([]byte(srcUrl))
	if err != nil {
		slog.Error(fmt.Sprintf("%s: %v", "Can't write url to w", err))
		os.Exit(1)
	}
}

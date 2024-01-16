package src

import (
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
	functions.HTTP("Src", Src)
}

const (
	srcUrl = "https://github.com/ArmandBriere/Archy"
)

func Src(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte(srcUrl))
}

package src

import (
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
	functions.HTTP("Src", Src)
}

func Src(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("https://github.com/ArmandBriere/Archy"))
}

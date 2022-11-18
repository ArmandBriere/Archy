package merch

import (
	"fmt"
	"net/http"
)

// Send the merch URL
func Merch(w http.ResponseWriter, r *http.Request) {
	message := "Oh you want some nice merch?\n*Every dollar I get will help me run faster and boost the Discord server*\n"
	message += "Go check my website <https://archyfroge.myshopify.com/>"
	fmt.Fprint(w, message)
}

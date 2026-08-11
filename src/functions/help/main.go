package help

import (
	"net/http"
	"strings"
)

// GetHelp describes all active commands
func GetHelp(w http.ResponseWriter, r *http.Request) {
	commands := []string{
		"!hello", "!describe", "!froge", "!gif", "!go", "!java", "!js", "!help",
		"!leaderboard", "!level", "!ban", "!warn", "!listwarn", "!answer",
		"!merch", "!video", "!exam", "!http", "!src", "!flag",
	}

	msg := "Active commands:\n" + strings.Join(commands, "\n")

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(msg))
}

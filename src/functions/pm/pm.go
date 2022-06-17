package pm

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/bwmarrin/discordgo"
)

func init() {
	functions.HTTP("pm", pm)
}

func pm(w http.ResponseWriter, r *http.Request) {
	var d struct {
		Message string `json:"message"`
		UserId  string `json:"user_id"`
	}

	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		switch err {
		case io.EOF:
			return
		default:
			log.Printf("json.NewDecoder: %v", err)
			http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
			return
		}
	}

	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return
	}

	channel, err := dg.UserChannelCreate(d.UserId)
	log.Printf("Sending to user " + d.UserId)
	log.Printf("message is " + d.Message)
	_, err = dg.ChannelMessageSend(channel.ID, d.Message)

	log.Printf("Done!")
}

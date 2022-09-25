package merch

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/bwmarrin/discordgo"
)

var Payload struct {
	ChannelId string `json:"channel_id"`
}

// Send the merch URL
func Merch(w http.ResponseWriter, r *http.Request) {
	// Parse body to get Payload
	var payload = Payload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		panic(err)
	}
	// Instanciate Discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session: ", err)
	}

	// Get the channel
	channel, err := dg.Channel(payload.ChannelId)
	if err != nil {
		panic("Unauthorized to create the connection. Verify Discord Token or ChannelID")
	}

	// Send message
	message, _ := dg.ChannelMessageSend(channel.ID, "https://archyfroge.myshopify.com/")

	// React to it
	err = dg.MessageReactionAdd(channel.ID, message.ID, "💸")
	if err != nil {
		panic(err)
	}
}

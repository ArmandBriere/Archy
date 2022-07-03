package welcome

import (
	"encoding/json"
	"fmt"
	"html"
	"net/http"
	"strings"
	"os"

	"github.com/bwmarrin/discordgo"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

type Payload struct {
	UserId  string `json:"user_id"`
	Username string `json:"username"`
	ServerId string `json:"server_id"`
	ServerName string `json:"server_name"`
	AvatarUrl string `json:"avatar_url"`
	ChannelId string `json:"channel_id"`
}

func GreetingNewMember(w http.ResponseWriter, r *http.Request) {
	//Parse body to get Payload
	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)

	if err != nil {
		panic(err)
	}

	if len(payload.UserId) == 0 
	or len(payload.Username) == 0 
	or len(payload.ServerName) == 0 
	or len(payload.AvatarUrl) == 0 {
		panic("Missing data in payload")
	}

	// Instantiate Discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session: ", err)
	}

	// Get the channel
	channel, err := dg.Channel(payload.ChannelId)
	if err != nil {
		panic("Unauthorized to create the connection. Verify Discord Token or ChannelID")
	}

	//Build a string efficiently with strings.Builder
	var message strings.Builder
	url.WriteString("Hey {}, welcome to {}!\n", payload.Username, payload.ServerName)
	url.WriteString("Check out the <#{}> and have fun!.\n", payload.ServerId)

	//TODO: Add a screenshot of the new member avatar like with 
	//code ...

	// Send message
	message, _ := dg.ChannelMessageSend(channel.ID, "Golang is faster!")
}

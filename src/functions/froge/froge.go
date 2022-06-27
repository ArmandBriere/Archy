package froge

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"regexp"
	"time"

	"github.com/bwmarrin/discordgo"
)

var Payload struct {
	ChannelId string `json:"channel_id"`
	ServerId  string `json:"server_id"`
}

// Send a Random Froge emoji from the server to the selected channel
func SendRandomFroge(w http.ResponseWriter, r *http.Request) {
	// Parse body to get Payload
	var payload = Payload
	json.NewDecoder(r.Body).Decode(&payload)

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

	// Prepare a list to store selected Froge
	var frogeEmojis []*discordgo.Emoji

	// Get all server emojis
	emojis, _ := dg.GuildEmojis(payload.ServerId)
	for _, emoji := range emojis {
		r := regexp.MustCompile("froge")
		// Select Froge only
		if r.MatchString(emoji.Name) {
			frogeEmojis = append(frogeEmojis, emoji)
		}
	}

	// Select a random Froge
	rand.Seed(time.Now().Unix())
	randomFroge := frogeEmojis[rand.Intn(len(frogeEmojis))]

	// Select extension to enable gif support
	frogeExtension := ".webp"
	if randomFroge.Animated {
		frogeExtension = ".gif"
	}

	// Send the Froge
	bigFrogeUrl := "https://cdn.discordapp.com/emojis/" + randomFroge.ID + frogeExtension
	dg.ChannelMessageSend(channel.ID, bigFrogeUrl)

}

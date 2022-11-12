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
	ServerId string `json:"server_id"`
}

// Return a Random Froge emoji from the server
func SendRandomFroge(w http.ResponseWriter, r *http.Request) {
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

	// Prepare a list to store selected Froge
	var frogeEmojis []*discordgo.Emoji

	// Get all server emojis
	emojis, _ := dg.GuildEmojis(payload.ServerId)
	for _, emoji := range emojis {
		r := regexp.MustCompile("froge")

		if r.MatchString(emoji.Name) {
			frogeEmojis = append(frogeEmojis, emoji)
		}
	}

	// Select a random Froge
	rand.Seed(time.Now().UnixNano())
	randomFroge := frogeEmojis[rand.Intn(len(frogeEmojis))]

	// Select extension to enable gif support
	frogeExtension := ".webp"
	if randomFroge.Animated {
		frogeExtension = ".gif"
	}

	// Send the Froge
	bigFrogeUrl := "https://cdn.discordapp.com/emojis/" + randomFroge.ID + frogeExtension

	fmt.Fprint(w, bigFrogeUrl)
}

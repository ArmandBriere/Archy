package welcome

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"

	"github.com/bwmarrin/discordgo"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

// Payload struct that is expected
type Payload struct {
	UserId     string `json:"user_id"`
	Username   string `json:"username"`
	ServerId   string `json:"server_id"`
	ServerName string `json:"server_name"`
	AvatarUrl  string `json:"avatar_url"`
	ChannelId  string `json:"channel_id"`
}

// User expected format in firestore
type FirestoreUser struct {
	Username  string `firestore:"username"`
	AvatarUrl string `firestore:"avatar_url"`
}

// Unmarshal received context and call proper function that send message
func GreetingNewMember(ctx context.Context, m PubSubMessage) error {
	log.Printf("Starting!")

	// Unmarshal data to a valid payload
	var payload Payload
	json.Unmarshal(m.Data, &payload)

	if len(payload.UserId) == 0 ||
		len(payload.Username) == 0 ||
		len(payload.ServerName) == 0 ||
		len(payload.AvatarUrl) == 0 {
		panic("Missing data in payload")
	}

	return SendGreetingNewMember(&payload)
}

// Send a welcome message to a new member
func SendGreetingNewMember(payload *Payload) error {

	// Instantiate discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))

	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return err
	}

	// Instantiate a direct message channel
	channel, err := dg.Channel(payload.ChannelId)

	if err != nil {
		error_message := []byte(err.Error())
		error_400_regex, _ := regexp.Compile("400")
		if len(error_400_regex.Find(error_message)) > 0 {
			panic("Can't create Channel - Bad ChannelId")
		}
		error_401_regex, _ := regexp.Compile("401")
		if len(error_401_regex.Find(error_message)) > 0 {
			panic("Unauthorized to create the connection. Verify Discord Token")
		}
		return err
	}

	// Create Message object
	var messageData discordgo.MessageSend
	messageData.Content = BuildWelcomeMessage(payload)

	// Send welcome message to new member into the channel intended
	log.Printf("Sending to channel: " + payload.ChannelId)
	log.Printf("Message: " + messageData.Content)
	_, err = dg.ChannelMessageSendComplex(channel.ID, &messageData)

	if err != nil {
		panic("Message didn't make it" + err.Error())
	}

	log.Printf("Done!")
	return nil
}

//Build a welcome message  - efficiently with strings.Builder
func BuildWelcomeMessage(payload *Payload) string {

	var messageWelcome strings.Builder
	messageWelcome.WriteString(fmt.Sprintf("Hey %s, welcome to %s!\n", payload.Username, payload.ServerName))
	messageWelcome.WriteString(fmt.Sprintf("Check out the <#%s> and have fun!.\n", payload.ChannelId))

	return messageWelcome.String()
}

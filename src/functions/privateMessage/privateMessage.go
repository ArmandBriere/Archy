package privateMessage

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"

	"github.com/bwmarrin/discordgo"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

// Payload struct that is expected
type Payload struct {
	UserId  string `json:"user_id"`
	Message string `json:"message"`
	Image   string `json:"image"`
}

// Unmarshal received context and call proper function that send message
func PrivateMessage(ctx context.Context, m PubSubMessage) error {

	log.Printf("Starting!")

	// Unmarshal data to a valid payload
	var payload Payload
	err := json.Unmarshal(m.Data, &payload)
	if err != nil {
		panic(err)
	}

	return SendPrivateMessage(&payload)
}

// Send a private message to the selected user
func SendPrivateMessage(payload *Payload) error {

	// Instanciate discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return err
	}

	// Instanciate a direct message channel
	channel, err := dg.UserChannelCreate(payload.UserId)

	if err != nil {
		error_message := []byte(err.Error())
		error_400_regex, _ := regexp.Compile("400")
		if len(error_400_regex.Find(error_message)) > 0 {
			panic("Can't create UserChannel - Bad UserId")
		}
		error_401_regex, _ := regexp.Compile("401")
		if len(error_401_regex.Find(error_message)) > 0 {
			panic("Unauthorized to create the connection. Verify Discord Token")
		}
		return err
	}

	// Create Message object
	var messageData discordgo.MessageSend
	messageData.Content = payload.Message
	// Create file reader for image
	imageAsBytes, _ := base64.StdEncoding.DecodeString(payload.Image)

	// Add the image only if it is provided
	if len(imageAsBytes) > 0 {
		reader := bytes.NewReader(imageAsBytes)
		var file discordgo.File
		var files []*discordgo.File = []*discordgo.File{&file}

		files[0].Name = "image.png"
		files[0].ContentType = "png"
		files[0].Reader = reader

		messageData.Files = files
	}

	// Send message to user
	log.Printf("Sending to user: " + payload.UserId)
	log.Printf("Message is: " + payload.Message)
	log.Printf("Image was send with it: " + strconv.FormatBool(len(imageAsBytes) > 0))
	_, err = dg.ChannelMessageSendComplex(channel.ID, &messageData)

	if err != nil {
		error_message := []byte(err.Error())
		error_403_regex, _ := regexp.Compile("403")
		if len(error_403_regex.Find(error_message)) > 0 {
			log.Printf("User " + payload.UserId + " is in private mode. We can't send a message to him.")
			return nil
		}
		panic("Message didn't make it" + err.Error())
	}

	log.Printf("Done!")
	return nil
}

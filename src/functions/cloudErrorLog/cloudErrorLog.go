package clouderrorlog

import (
	"context"
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
	TextPayload string `json:"textPayload"`
	Resource    struct {
		Type   string `json:"type"`
		Labels struct {
			FunctionName string `json:"function_name"`
			Region       string `json:"region"`
			ProjectId    string `json:"project_id"`
		}
	}
	Timestamp string `json:"timestamp"`
	Severity  string `json:"severity"`
}

// Unmarshal received context and call proper function that send message
func UnmarshalPubsubMessage(ctx context.Context, m PubSubMessage) error {
	log.Printf("Starting!")

	// Unmarshal data to a valid payload
	var payload Payload
	err := json.Unmarshal(m.Data, &payload)
	if err != nil {
		panic(err)
	}

	return SendErrorLogToDiscordChannel(&payload)
}

// Create a nice embed message and send it with selected data
func SendErrorLogToDiscordChannel(payload *Payload) error {

	// Instanciate discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return err
	}

	// Instanciate a direct message channel with the Log channel of the Discord
	channel, err := dg.Channel("991158032509698169")

	if err != nil {
		errorMessage := []byte(err.Error())
		error400Regex, _ := regexp.Compile("400")
		if len(error400Regex.Find(errorMessage)) > 0 {
			panic("Can't create Channel - Bad ChannelId")
		}
		error401Regex, _ := regexp.Compile("401")
		if len(error401Regex.Find(errorMessage)) > 0 {
			panic("Unauthorized to create the connection. Verify Discord Token")
		}
		return err
	}

	// Create Embed message
	messageData := createEmbedMessage(payload)

	// Sending message
	message, err := dg.ChannelMessageSendEmbed(channel.ID, &messageData)

	if err != nil {
		panic("Message didn't make it" + err.Error())
	}

	_, err = dg.MessageThreadStart(message.ChannelID, message.ID, messageData.Title, 1440)
	if err != nil {
		panic(nil)
	}

	log.Printf("Done!")
	return nil
}

// Create the Embed message according to the payload data
func createEmbedMessage(payload *Payload) discordgo.MessageEmbed {

	// Create Embed message
	var messageEmbed discordgo.MessageEmbed

	// Setup title and description
	messageEmbed.Title = payload.Severity + " in " + payload.Resource.Type + " " + payload.Resource.Labels.FunctionName
	messageEmbed.Description = payload.Resource.Labels.ProjectId + " - " + payload.Resource.Labels.Region

	// Color palette of Discord: https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
	switch {
	case payload.Severity == "ERROR":
		messageEmbed.Color = 16705372 // Yellow
	case payload.Severity == "CRITICAL":
		messageEmbed.Color = 15418782 // Fuschia
	case payload.Severity == "ALERT":
		messageEmbed.Color = 11027200 // Dark orange
	case payload.Severity == "EMERGENCY":
		messageEmbed.Color = 10038562 // Dark red
	}

	// Split message into 1024 (1018 + backticks) chunk (discord limitation)
	var messageSlices = splitByWidth(payload.TextPayload, 1018)
	for index, text := range messageSlices {
		var messageField discordgo.MessageEmbedField
		messageField.Name = "Log part " + strconv.Itoa(index)
		messageField.Value = "```" + text + "```"
		messageEmbed.Fields = append(messageEmbed.Fields, &messageField)
	}

	// Add log timestamp
	messageEmbed.Timestamp = payload.Timestamp

	return messageEmbed
}

func splitByWidth(str string, size int) []string {
	strLength := len(str)

	var splited []string
	var stop int
	for i := 0; i < strLength; i += size {
		stop = i + size
		if stop > strLength {
			stop = strLength
		}
		splited = append(splited, str[i:stop])
	}

	return splited
}

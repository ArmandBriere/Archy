package clouddeploymentlog

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
type AuthenticationInfo struct {
	PrincipalEmail string `json:"principalEmail"`
}

type ProtoPayload struct {
	MethodName         string `json:"methodName"`
	AuthenticationInfo AuthenticationInfo
}

type Labels struct {
	FunctionName string `json:"function_name"`
	Region       string `json:"region"`
	ProjectId    string `json:"project_id"`
}

type Resource struct {
	Type   string `json:"type"`
	Labels Labels
}

type Payload struct {
	Timestamp    string `json:"timestamp"`
	Severity     string `json:"severity"`
	ProtoPayload ProtoPayload
	Resource     Resource
}

// Unmarshal received context and call proper function that send message
func UnmarshalPubsubMessage(ctx context.Context, m PubSubMessage) error {
	log.Printf("Starting!")

	var payload Payload
	err := json.Unmarshal(m.Data, &payload)
	if err != nil {
		panic(err)
	}

	return SendErrorLogToDiscordChannel(&payload)
}

// Create a nice embed message and send it with selected data
func SendErrorLogToDiscordChannel(payload *Payload) error {

	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return err
	}

	channel, err := dg.Channel("1092832808868790342")

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

	messageData := createEmbedMessage(payload)

	_, err = dg.ChannelMessageSendEmbed(channel.ID, &messageData)
	if err != nil {
		panic("Message didn't make it" + err.Error())
	}
	log.Printf("Done!")
	return nil
}

// Create the Embed message according to the payload data
func createEmbedMessage(payload *Payload) discordgo.MessageEmbed {

	var prefixMessage string

	if strings.Contains(payload.ProtoPayload.MethodName, "UpdateFunction") {
		prefixMessage = "A new version of this function is being deployed: "
	} else if strings.Contains(payload.ProtoPayload.MethodName, "CreateFunction") {
		prefixMessage = "A new function is being created: "
	}

	// Create Embed message
	var messageEmbed discordgo.MessageEmbed
	messageEmbed.Title = "Cloud function modification from: " + payload.ProtoPayload.AuthenticationInfo.PrincipalEmail
	messageEmbed.Description = prefixMessage + payload.Resource.Labels.FunctionName
	messageEmbed.Color = 16705372 // Yellow
	messageEmbed.Timestamp = payload.Timestamp

	return messageEmbed
}

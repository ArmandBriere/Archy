package stm

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"

	firestore "cloud.google.com/go/firestore"
	"cloud.google.com/go/pubsub"
	firebase "firebase.google.com/go"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

// Expected format by the 'channel_message_discord' function
type PubsubDataChannelMessage struct {
	ChannelId string `json:"channel_id"`
	Message   string `json:"message"`
}

// Expected format by the stm API
type StmStatus struct {
	Header struct {
		Timestamp string `json:"timestamp"`
	} `json:"header"`
	Alerts []struct {
		ActivePeriods []struct {
			Start int         `json:"start"`
			End   interface{} `json:"end"`
		} `json:"active_periods"`
		Cause            interface{} `json:"cause"`
		Effect           interface{} `json:"effect"`
		InformedEntities []struct {
			RouteShortName string `json:"route_short_name"`
		} `json:"informed_entities"`
		HeaderTexts []struct {
			Language string `json:"language"`
			Text     string `json:"text"`
		} `json:"header_texts"`
		DescriptionTexts []struct {
			Language string `json:"language"`
			Text     string `json:"text"`
		} `json:"description_texts"`
	} `json:"alerts"`
}

type StmLine struct {
	Name   string `firestore:"name"`
	Id     int    `firestore:"id"`
	Status string `firestore:"status"`
}

type Channels struct {
	ChannelsId []string `firestore:"channels_id"`
}

var ENVIRONMENT = strings.Split(os.Getenv("K_SERVICE"), "_")[0]
var STM_API_KEY = os.Getenv("STM_API_KEY")

const PROJECT_ID = "archy-f06ed"
const STM_API_URL = "https://api.stm.info/pub/od/i3/v1/messages/etatservice/"

var STM_LINES = []StmLine{
	{
		Name: "Green",
		Id:   1,
	},
	{
		Name: "Orange",
		Id:   2,
	},
	{
		Name: "Yellow",
		Id:   4,
	},
	{
		Name: "Blue",
		Id:   5,
	},
}

// Call STM api and compare the new and old status for selected lines
func CheckStmStatus(ctx context.Context, m PubSubMessage) error {
	newStmStatus := fetchStmStatus()

	var wg sync.WaitGroup
	wg.Add(len(STM_LINES))

	fmt.Println("Start multithreaded call...")
	for lineIndex := 0; lineIndex < len(STM_LINES); lineIndex++ {
		go updateStatus(newStmStatus, lineIndex, &wg)
	}
	wg.Wait()
	fmt.Println("Finish multithreaded")

	return nil
}

// Call STM api to get line status
func fetchStmStatus() StmStatus {
	req, err := http.NewRequest("GET", STM_API_URL, nil)
	req.Header.Set("apikey", STM_API_KEY)
	req.Header.Set("origin", ".")
	if err != nil {
		log.Fatalln(err)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln(err)
	}

	var stmStatus StmStatus
	err = json.NewDecoder(resp.Body).Decode(&stmStatus)

	if err != nil {
		log.Fatalln(err)
	}

	resp.Body.Close()
	return stmStatus
}

// Create the default STM status in firestore
func createDefaultStmStatusFirestore(currentLine StmLine) {
	fmt.Println("Create new default line status for " + currentLine.Name + " line")

	firestoreCtx, client := getFirestoreClientCtx()
	stmStatusRef := client.Collection("stm")

	_, err := stmStatusRef.Doc(strconv.Itoa(currentLine.Id)).Set(firestoreCtx, currentLine)
	if err != nil {
		panic(err)
	}
}

// Compare old and new status, update it and send channel message if needed
func updateStatus(newStmStatus StmStatus, lineIndex int, wg *sync.WaitGroup) {
	defer wg.Done()

	currentLine := STM_LINES[lineIndex]
	log.Printf("Start analysing STM status for line " + strconv.Itoa(currentLine.Id))

	var newStmStatusText string

	for _, alert := range newStmStatus.Alerts {
		if alert.InformedEntities[0].RouteShortName == strconv.Itoa(currentLine.Id) {

			newStmStatusText += alert.DescriptionTexts[1].Text + "\n"
		}
	}

	if newStmStatusText != "" {
		firestoreCtx, client := getFirestoreClientCtx()
		stmStatusRef := client.Collection("stm").Doc(strconv.Itoa(currentLine.Id))

		stmStatusDoc, err := stmStatusRef.Get(firestoreCtx)
		if err != nil {
			createDefaultStmStatusFirestore(currentLine)
			stmStatusDoc, _ = stmStatusRef.Get(firestoreCtx)
		}

		oldStatusText, err := stmStatusDoc.DataAt("status")
		if err != nil {
			panic(err)
		}

		if newStmStatusText != oldStatusText {
			_, err = stmStatusRef.Update(firestoreCtx, []firestore.Update{
				{
					Path:  "status",
					Value: newStmStatusText,
				},
			})
			if err != nil {
				panic(err)
			}

			newStmStatusText = "**STM update for the " + currentLine.Name + " line**\n" + newStmStatusText + "\n🎵 too doo doo 🎵"

			channels := getChannels()
			if channels != nil {
				publishChannelMessage(channels.ChannelsId, newStmStatusText)
			}
		}
	}

	log.Println("Done with line " + strconv.Itoa(currentLine.Id))
}

// Instantiate the Firestore client and context
func getFirestoreClientCtx() (context.Context, *firestore.Client) {
	firestoreCtx := context.Background()
	conf := &firebase.Config{ProjectID: PROJECT_ID}
	app, err := firebase.NewApp(firestoreCtx, conf)

	if err != nil {
		log.Fatalln(err)
	}

	client, err := app.Firestore(firestoreCtx)
	if err != nil {
		log.Fatalln(err)
	}

	return firestoreCtx, client
}

// Get all stm status channel from firebase
func getChannels() *Channels {
	firestoreCtx, client := getFirestoreClientCtx()
	channelsRef := client.Collection("stm").Doc("channel")
	channelsDoc, err := channelsRef.Get(firestoreCtx)
	if err != nil {
		fmt.Println("No stm channel were found")
		return nil
	}

	var channelsId Channels
	if err = channelsDoc.DataTo(&channelsId); err != nil {
		panic(err)
	}

	return &channelsId
}

// Publish a message to channel_message_discord
func publishChannelMessage(channels []string, message string) {
	firestoreCtx := context.Background()
	client, err := pubsub.NewClient(firestoreCtx, PROJECT_ID)
	if err != nil {
		panic(err)
	}
	defer client.Close()

	topicClient := client.Topic(ENVIRONMENT + "_channel_message_discord")

	for _, channelId := range channels {
		pubsubData, err := json.Marshal(PubsubDataChannelMessage{ChannelId: channelId, Message: message})
		if err != nil {
			panic(err)
		}

		result := topicClient.Publish(firestoreCtx, &pubsub.Message{
			Data: []byte(pubsubData),
		})

		messageId, err := result.Get(firestoreCtx)
		if err != nil {
			panic(err)
		}

		log.Println("Message send to topic, messageId: " + messageId)
	}
}

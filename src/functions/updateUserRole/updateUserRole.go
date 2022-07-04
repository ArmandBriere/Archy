package updateuserrole

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go"
	"google.golang.org/api/iterator"

	"github.com/bwmarrin/discordgo"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

// Payload struct that is expected
type Payload struct {
	ServerId string `json:"server_id"`
	UserId   string `json:"user_id"`
}

// Role expected format in firestore
type FirestoreRole struct {
	Roles []string `firestore:"roles"`
}

// User expected format in firestore
type FirestoreUser struct {
	Level    int    `firestore:"level"`
	Username string `firestore:"username"`
}

// Unmarshal received context and call proper function that send message
func UserRole(ctx context.Context, m PubSubMessage) error {

	log.Printf("Starting!")

	// Unmarshal data to a valid payload
	var payload Payload
	err := json.Unmarshal(m.Data, &payload)
	if err != nil {
		panic(err)
	}

	return UpdateUserRole(&payload)
}

// Update the user role base on his level in firestore
func UpdateUserRole(payload *Payload) error {

	// Instanciate discord bot
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return err
	}

	// Instanciate the firestore context
	ctx := context.Background()
	conf := &firebase.Config{ProjectID: "archy-f06ed"}
	app, err := firebase.NewApp(ctx, conf)

	if err != nil {
		log.Fatalln(err)
	}

	client, err := app.Firestore(ctx)
	if err != nil {
		log.Fatalln(err)
	}

	// Get the user level on firestore
	userRef, err := client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId).Get(ctx)
	if err != nil {
		panic(err)
	}
	var user FirestoreUser
	err = userRef.DataTo(&user)
	if err != nil {
		panic(err)
	}

	expectedRoles := getExpectedRoles(client, *payload, ctx, user)

	// Loop over the roles and give them to the user
	for _, roleId := range expectedRoles {
		log.Print("Adding role " + roleId + " to user " + user.Username)

		err := dg.GuildMemberRoleAdd(payload.ServerId, payload.UserId, roleId)
		if err != nil {
			panic(err)
		}
	}

	// Disconnect client and done
	log.Print("Done!")
	defer client.Close()
	return nil
}

// Get the roles that a user should have based on his level in firestore
func getExpectedRoles(client *firestore.Client, payload Payload, ctx context.Context, user FirestoreUser) []string {
	var expectedRoles []string
	iter := client.Collection("servers").Doc(payload.ServerId).Collection("levels").Documents(ctx)
	for {
		doc, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatalf("Failed to iterate: %v", err)
		}

		docId, _ := strconv.Atoi(doc.Ref.ID)
		if user.Level >= docId {

			var roles FirestoreRole
			if err := doc.DataTo(&roles); err != nil {
				panic(err)
			}
			expectedRoles = append(expectedRoles, roles.Roles...)
		}
	}
	return expectedRoles
}

package warn

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"regexp"
	"time"

	"cloud.google.com/go/pubsub"
	firebase "firebase.google.com/go"
	"github.com/bwmarrin/discordgo"
)

// Payload struct that is expected
type Payload struct {
	ServerId string   `json:"server_id"`
	UserId   string   `json:"user_id"`
	Mentions []string `json:"mentions"`
	Comment  string   `json:"params"`
}

type Warning struct {
	UserId        string    `firestore:"user_id,omitempty"`
	AdminId       string    `firestore:"admin_id,omitempty"`
	AdminUsername string    `firestore:"admin_username,omitempty"`
	Comment       string    `firestore:"user_id,omitempty"`
	Timestamp     time.Time `firestore:"timestamp,omitempty"`
}

// Admin only: Warn a user, ban him after 3 warn
func WarnUser(w http.ResponseWriter, r *http.Request) {

	// Parse body to get Payload
	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		panic(err)
	}

	// Instanciate Discord bot
	dg := instanciateBot()

	// Check admin permission
	isAdmin := isInvokingUserAnAdmin(dg, &payload)
	if !isAdmin {
		log.Printf(payload.UserId + " is NOT an admin!")
		return
	}
	log.Printf(payload.UserId + " is an admin!")

	log.Printf("Comment: " + payload.Comment)

	var newWarn = Warning{
		UserId:        payload.Mentions[0],
		AdminId:       payload.UserId,
		AdminUsername: getAdminUsername(dg, payload.UserId),
		Comment:       payload.Comment,
		Timestamp:     time.Now(),
	}

	var warnCount = writeWarnInFirestore(payload.ServerId, newWarn)

	sendWarnToUser(newWarn)

	takeAction(warnCount, newWarn)
}

func getAdminUsername(dg *discordgo.Session, userId string) string {
	user, _ := dg.User(userId)
	return user.Username
}

// Add the new warn to the database and return the number of warnings for this user
func writeWarnInFirestore(serverId string, warn Warning) int {
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
	defer client.Close()

	warnings := client.Collection("servers").Doc(serverId).Collection("warnings")

	_, err = warnings.NewDoc().Set(ctx, warn)

	if err != nil {
		panic(err)
	}

	query := warnings.Where("user_id", "==", warn.UserId)

	docs, _ := query.Documents(ctx).GetAll()

	return len(docs)
}

type PubsubData struct {
	UserId  string `json:"user_id"`
	Message string `json:"message"`
}

// Send a private message to the user to inform him
func sendWarnToUser(warn Warning) {
	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, "archy-f06ed")
	if err != nil {
		panic(err)
	}
	defer client.Close()

	topicClient := client.Topic("private_message_discord")

	message := "Hi, this message is a warning from this server: <Server name>." +
		"Please follow the code of conduct. \n" +
		"Here is the message from the admins:\n" + warn.Comment + "\n" +
		"Reminder: 3 warnings => 24h mute, 5 warnings => 1 week ban, 10 warnings => Life ban."

	pubsubData, err := json.Marshal(PubsubData{UserId: warn.UserId, Message: message})
	if err != nil {
		panic(err)
	}

	result := topicClient.Publish(ctx, &pubsub.Message{
		Data: []byte(pubsubData),
	})

	messageId, err := result.Get(ctx)
	if err != nil {
		panic(err)
	}

	log.Printf("Message send to user, id: " + messageId)
}

func takeAction(warnCount int, warn Warning) {
	// Nothing for now, will implement this after it the rest works
}

// Instanciate the bot and return the session
func instanciateBot() *discordgo.Session {
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))

	if err != nil {
		error_message := []byte(err.Error())
		error_400_regex, _ := regexp.Compile("400")
		if len(error_400_regex.Find(error_message)) > 0 {
			panic("Can't create bot instance - Bad ChannelId")
		}
		error_401_regex, _ := regexp.Compile("401")
		if len(error_401_regex.Find(error_message)) > 0 {
			panic("Unauthorized to create the connection. Verify Discord Token")
		}
		panic(err)
	}
	return dg
}

// Check if the user invoking this command is an admin
func isInvokingUserAnAdmin(dg *discordgo.Session, payload *Payload) bool {

	member, err := dg.GuildMember(payload.ServerId, payload.UserId)
	if err != nil {
		panic(err)
	}

	userRoles := member.Roles
	guildRole, _ := dg.GuildRoles(payload.ServerId)

	for _, v := range guildRole {
		if (v.Permissions & discordgo.PermissionAdministrator) == discordgo.PermissionAdministrator {

			for _, b := range userRoles {
				if b == v.ID {
					return true
				}
			}
		}
	}

	return false
}

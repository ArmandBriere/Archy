package warn

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	"cloud.google.com/go/pubsub"
	firebase "firebase.google.com/go"
	"github.com/bwmarrin/discordgo"
)

// Payload struct that is expected
type Payload struct {
	ServerId   string   `json:"server_id"`
	ServerName string   `json:"server_name"`
	UserId     string   `json:"user_id"`
	Mentions   []string `json:"mentions"`
	Comment    []string `json:"params"`
}

type Warning struct {
	ServerId      string    `firestore:"server_id,omitempty"`
	UserId        string    `firestore:"user_id,omitempty"`
	AdminId       string    `firestore:"admin_id,omitempty"`
	AdminUsername string    `firestore:"admin_username,omitempty"`
	Comment       string    `firestore:"comment,omitempty"`
	Timestamp     time.Time `firestore:"timestamp,omitempty"`
}

var ServerName string
var Dg *discordgo.Session

// Admin only: Warn a user, ban him after 3 warn
func WarnUser(w http.ResponseWriter, r *http.Request) {

	// Parse body to get Payload
	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		panic(err)
	}

	ServerName = payload.ServerName

	// Instanciate Discord bot
	Dg = instanciateBot()

	// Check admin permission
	isAdmin := isInvokingUserAnAdmin(&payload)
	if !isAdmin {
		log.Printf(payload.UserId + " is NOT an admin!")
		return
	}
	log.Printf(payload.UserId + " is an admin!")

	log.Printf("Comment: " + strings.Join(payload.Comment, " "))

	userId := payload.Mentions[0]
	comment := strings.Join(payload.Comment, " ")
	var newWarn = Warning{
		ServerId:      payload.ServerId,
		UserId:        userId,
		AdminId:       payload.UserId,
		AdminUsername: getAdminUsername(payload.UserId),
		Comment:       comment,
		Timestamp:     time.Now(),
	}

	var warnCount = writeWarnInFirestore(payload.ServerId, newWarn)

	sendWarnToUser(warnCount, newWarn)

	takeAction(warnCount, newWarn)
}

func getAdminUsername(userId string) string {
	user, _ := Dg.User(userId)
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
func sendWarnToUser(warnCount int, warn Warning) {
	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, "archy-f06ed")
	if err != nil {
		panic(err)
	}
	defer client.Close()

	topicClient := client.Topic("private_message_discord")

	message := "Hi, this message is a warning from this server: **" + ServerName + "**.\n" +
		"*Please follow the code of conduct.*\n\n" +
		"**Explanation:**\n" +
		warn.Comment + "\n\n" +
		"Number of warnings that you currently have on this server: " + strconv.Itoa(warnCount) + "\n\n" +
		"**Reminder:**\n" +
		"3 warnings → 24h mute.\n5 warnings → 1 week mute.\n10 warnings → Life ban."

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

	log.Printf("Message send to user, messageId: " + messageId)
}

func takeAction(warnCount int, warn Warning) {
	// Nothing for now, will implement this after it the rest works

	log.Printf("The user " + warn.UserId + " has " + strconv.Itoa(warnCount) + " warnings")

	if warnCount == 3 {
		muteForADay(warn)
	} else if warnCount == 5 {
		muteForAWeek(warn)
	} else if warnCount == 10 {
		banForLife(warn)
	}
}

func muteForADay(warn Warning) {
	log.Printf("The user " + warn.UserId + " is muted for a day on " + ServerName)
	tomorrow := time.Now().AddDate(0, 0, 1)
	Dg.GuildMemberTimeout(warn.ServerId, warn.UserId, &tomorrow)
}

func muteForAWeek(warn Warning) {
	log.Printf("The user " + warn.UserId + " is ban for a week on " + ServerName)
	inAWeek := time.Now().AddDate(0, 0, 7)
	Dg.GuildMemberTimeout(warn.ServerId, warn.UserId, &inAWeek)
}

func banForLife(warn Warning) {
	log.Printf("The user " + warn.UserId + " is ban for life on " + ServerName)
	Dg.GuildBanCreate(warn.ServerId, warn.UserId, 1)
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
func isInvokingUserAnAdmin(payload *Payload) bool {

	member, err := Dg.GuildMember(payload.ServerId, payload.UserId)
	if err != nil {
		log.Printf("Can't get this guild member for serverId: " + payload.ServerId + ". UserId: " + payload.UserId)
		panic(err)
	}

	userRoles := member.Roles
	guildRole, _ := Dg.GuildRoles(payload.ServerId)

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

package warn

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"regexp"
	"time"

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

	warnings := client.Collection("servers").Doc(serverId).Collection("warnings")

	_, err = warnings.NewDoc().Set(ctx, warn)

	if err != nil {
		panic(err)
	}

	query := warnings.Where("user_id", "==", warn.UserId)

	docs, _ := query.Documents(ctx).GetAll()
	defer client.Close()

	return len(docs)
}

func sendWarnToUser(warn Warning) {

}

func takeAction(warnCount int, warn Warning) {

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

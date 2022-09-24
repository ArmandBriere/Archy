package listwarn

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go"
	"github.com/bwmarrin/discordgo"
	"google.golang.org/api/iterator"
)

type Payload struct {
	ServerId   string `json:"server_id"`
	ServerName string `json:"server_name"`
	UserId     string `json:"user_id"`
}

type Warning struct {
	ServerId      string    `firestore:"server_id,omitempty"`
	UserId        string    `firestore:"user_id,omitempty"`
	AdminId       string    `firestore:"admin_id,omitempty"`
	AdminUsername string    `firestore:"admin_username,omitempty"`
	Comment       string    `firestore:"comment,omitempty"`
	Timestamp     time.Time `firestore:"timestamp,omitempty"`
}

var Dg *discordgo.Session

// Admin only: List every warn of the server
func ListWarn(w http.ResponseWriter, r *http.Request) {

	var payload = Payload{}
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		panic(err)
	}

	if len(payload.ServerId) == 0 ||
		len(payload.ServerName) == 0 ||
		len(payload.UserId) == 0 {
		fmt.Fprint(w, "Please use the correct format: `!listwarn`")
		return
	}

	Dg = instanciateBot()

	isAdmin := isInvokingUserAnAdmin(&payload)
	if !isAdmin {
		log.Printf(payload.UserId + " is NOT an admin!")
		return
	}
	log.Printf(payload.UserId + " is an admin!")

	fmt.Fprint(w, generateWarnList(payload.ServerId))
}

func generateWarnList(serverId string) string {
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

	warningIter := client.Collection("servers").Doc(serverId).Collection("warnings").OrderBy("user_id", firestore.Asc).Documents(ctx)

	var data strings.Builder
	for {
		doc, err := warningIter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			panic(err)
		}

		var warn Warning

		err = doc.DataTo(&warn)
		if err != nil {
			panic(err)
		}

		data.WriteString("**")
		data.WriteString(warn.Timestamp.Format("2006-02-01"))
		data.WriteString("**\n")
		data.WriteString("User: <@")
		data.WriteString(warn.UserId)
		data.WriteString(">")
		data.WriteString(" - By <@")
		data.WriteString(warn.AdminId)
		data.WriteString(">\n")
		data.WriteString("Comment: ")
		data.WriteString(warn.Comment)
		data.WriteString("\n\n")

		fmt.Println(doc.Data())
	}

	if len(data.String()) == 0 {
		return "What a nice server, not a single user received a warning!"
	}

	return data.String()
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

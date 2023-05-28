package ban

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"regexp"

	"github.com/bwmarrin/discordgo"
)

// Payload struct that is expected
type Payload struct {
	ServerId string   `json:"server_id"`
	UserId   string   `json:"user_id"`
	Mentions []string `json:"mentions"`
}

// Admin only: Ban a user
func BanUser(w http.ResponseWriter, r *http.Request) {

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

	// Ban user
	if len(payload.Mentions) == 1 {
		err := dg.GuildBanCreate(payload.ServerId, payload.Mentions[0], 0)

		if err != nil {
			panic("Ban didn't work " + err.Error())
		}
		log.Printf("User " + payload.Mentions[0] + " has been banned!")
	} else {
		log.Printf("Mentions should be of len 1")
	}

}

// Instanciate the bot and return the session
func instanciateBot() *discordgo.Session {
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))

	if err != nil {
		errorMessage := []byte(err.Error())
		error400Regex, _ := regexp.Compile("400")
		if len(error400Regex.Find(errorMessage)) > 0 {
			panic("Can't create bot instance - Bad ChannelId")
		}
		error401Regex, _ := regexp.Compile("401")
		if len(error401Regex.Find(errorMessage)) > 0 {
			panic("Unauthorized to create the connection. Verify Discord Token")
		}
		panic(err)
	}
	return dg
}

// Check if the user invoking this command is an admin
func isInvokingUserAnAdmin(dg *discordgo.Session, payload *Payload) bool {
	//Get the invoking user
	member, err := dg.GuildMember(payload.ServerId, payload.UserId)
	if err != nil {
		panic(err)
	}

	userRoles := member.Roles
	guildRole, _ := dg.GuildRoles(payload.ServerId)

	// Check if the user has Administrator permission in any of his role
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

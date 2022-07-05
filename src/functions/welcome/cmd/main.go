package main

import (
	welcome "welcome.com/cloudfunction"
)

func main() {
	//Add custom server_id to test
	payload := welcome.Payload{
		UserId:     "<USER_ID>",
		Username:   "<USERNAME>",
		ServerId:   "<SERVER_ID>",
		ServerName: "<SERVER_NAME>",
		AvatarUrl:  "<AVATAR_URL>",
		ChannelId:  "<CHANNEL_ID>",
	}

	// Call function
	welcome.SendGreetingNewMember(&payload)
}

package main

import (
	privateMessage "updateUserRole.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	payload := privateMessage.Payload{
		ServerId: "<SERVER_ID>",
		UserId:   "<USER_ID>",
	}

	err := privateMessage.UpdateUserRole(&payload)
	if err != nil {
		panic(err)
	}
}

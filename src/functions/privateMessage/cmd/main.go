package main

import (
	privateMessage "privateMessage.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	payload := privateMessage.Payload{
		UserId:  "<USER_ID>",
		Message: "Simple private message",
		// Dummy image to validate that it was send
		Image: "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
	}

	privateMessage.SendPrivateMessage(&payload)
}

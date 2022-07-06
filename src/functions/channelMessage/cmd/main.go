package main

import (
	channelMessage "channelMessage.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	payload := channelMessage.Payload{
		ChannelId: "<CHANNEL_ID>",
		Message:   "Simple channel message",
		// Dummy image to validate that it was send
		Image: "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
	}

	err := channelMessage.SendChannelMessage(&payload)
	if err != nil {
		panic(err)
	}
}

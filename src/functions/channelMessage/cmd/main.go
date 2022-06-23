package main

import (
	channelMessage "channelMessage.com/cloudfunction"
)

func main() {

	payload := channelMessage.Payload{
		ChannelId: "977433515962544149",
		Message:   "Simple channel message",
		Image:     "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
	}
	channelMessage.SendChannelMessage(&payload)
}

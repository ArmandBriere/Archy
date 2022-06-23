package main

import (
	privateMessage "privateMessage.com/cloudfunction"
)

func main() {

	payload := privateMessage.Payload{
		UserId:  "135048445097410560",
		Message: "Simple private message",
		Image:   "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
	}
	privateMessage.SendPrivateMessage(&payload)
}

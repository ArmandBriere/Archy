package exp

import (
	"context"
	"encoding/json"
)

// Data struct from Pubsub
type PubSubMessage struct {
	Data []byte `json:"data"`
}

// `json:"channel_id"`
type Payload struct {
	UserId     string `json:"user_id"`
	Username   string `json:"username"`
	AvatarUrl  string `json:"avatar_url"`
	ServerId   string `json:"server_id"`
	ServerName string `json:"server_name"`
}

type MissingData struct{}

func (m *MissingData) Error() string {
	return "Missing data"
}

// Increase the user experience on firestore
func Exp(ctx context.Context, m PubSubMessage) error {
	var payload Payload
	err := json.Unmarshal(m.Data, &payload)
	if err != nil {
		panic(err)
	}

	if len(payload.UserId) == 0 ||
		len(payload.Username) == 0 ||
		len(payload.AvatarUrl) == 0 ||
		len(payload.ServerId) == 0 ||
		len(payload.ServerName) == 0 {
		return &MissingData{}
	}

	return nil
}

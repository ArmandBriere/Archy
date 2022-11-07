package exp

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/rand"
	"strconv"
	"time"

	"cloud.google.com/go/firestore"
	"cloud.google.com/go/pubsub"
	firebase "firebase.google.com/go"
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

// User expected format in firestore
type FirestoreUser struct {
	Username           string `firestore:"username"`
	Level              int    `firestore:"level"`
	AvatarUrl          string `firestore:"avatar_url"`
	ExpTowardNextLevel int    `firestore:"exp_toward_next_level"`
	TotalExp           int    `firestore:"total_exp"`
	LevelExpNeeded     float64
}

// Data format expected by the 'private_message_discord' function
type PubsubDataPrivateMessage struct {
	UserId  string `json:"user_id"`
	Message string `json:"message"`
}

// Custom error for missing data in payload
type MissingData struct{}

func (m *MissingData) Error() string {
	return "Missing data from pubsub payload"
}

const DATETIME_FORMAT_EXAMPLE = "2006-01-02 15:04:05"

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

	firestoreCtx, client := getFirestoreClientCtx(payload)
	_, err = client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId).Get(firestoreCtx)
	if err != nil {
		createUser(payload)
	}

	if verifyTimestamp(payload) {
		user := getAllUserInfo(payload)

		newUser := addExpToUser(user, payload)

		if user.Level != newUser.Level {
			sendPrivateMessage(payload.UserId, "I'm so proud of you... You made it to level "+strconv.Itoa(newUser.Level)+" in "+payload.ServerName+"!")
		}
	}

	return nil
}

// Verify that last message was send more than one minute ago
func verifyTimestamp(payload Payload) bool {
	lastMessageTimestamp := getLastMessageTimestamp(payload)

	timeStamp, err := time.Parse(DATETIME_FORMAT_EXAMPLE, lastMessageTimestamp)

	if err != nil {
		return false
	}

	timeDiff := time.Since(timeStamp)

	if timeDiff.Seconds() < 60 {
		fmt.Print("Exit: Too soon - " + timeDiff.String())
		return false
	}

	return true
}

func getFirestoreClientCtx(payload Payload) (context.Context, *firestore.Client) {
	firestoreCtx := context.Background()
	conf := &firebase.Config{ProjectID: "archy-f06ed"}
	app, err := firebase.NewApp(firestoreCtx, conf)

	if err != nil {
		log.Fatalln(err)
	}

	client, err := app.Firestore(firestoreCtx)
	if err != nil {
		log.Fatalln(err)
	}

	return firestoreCtx, client
}

// Get last message timestamp of user
func getLastMessageTimestamp(payload Payload) string {
	firestoreCtx, client := getFirestoreClientCtx(payload)
	userRef, err := client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId).Get(firestoreCtx)
	if err != nil {
		panic(err)
	}

	timestamp, err := userRef.DataAt("last_message_timestamp")
	if err != nil {
		panic(err)
	}

	return fmt.Sprint(timestamp)
}

// Get the user info from Firestore
func getAllUserInfo(payload Payload) FirestoreUser {
	firestoreCtx, client := getFirestoreClientCtx(payload)

	userRef, err := client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId).Get(firestoreCtx)
	if err != nil {
		panic(err)
	}
	var user FirestoreUser

	err = userRef.DataTo(&user)
	if err != nil {
		panic(err)
	}

	user.LevelExpNeeded = (5 * math.Pow(float64(user.Level), 2)) + (50 * float64(user.Level)) + 100

	return user
}

func createUser(payload Payload) {
	fmt.Println("Create new user " + payload.UserId)

	firestoreCtx, client := getFirestoreClientCtx(payload)
	userRef := client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId)

	err := client.RunTransaction(firestoreCtx, func(ctx context.Context, tx *firestore.Transaction) error {
		return tx.Set(userRef, map[string]interface{}{
			"total_exp":              0,
			"exp_toward_next_level":  0,
			"level":                  0,
			"message_count":          0,
			"username":               payload.Username,
			"avatar_url":             payload.AvatarUrl,
			"last_message_timestamp": time.Now().Format(DATETIME_FORMAT_EXAMPLE),
		}, firestore.MergeAll)
	})
	if err != nil {
		panic(err)
	}
}

// Add exp to user
func addExpToUser(user FirestoreUser, payload Payload) FirestoreUser {

	rand.Seed(time.Now().UnixNano())

	addedExp := rand.Intn(75-45) + 45
	fmt.Println("Added exp " + strconv.Itoa(addedExp))
	ctx, client := getFirestoreClientCtx(payload)
	userRef, err := client.Collection("servers").Doc(payload.ServerId).Collection("users").Doc(payload.UserId).Get(ctx)
	if err != nil {
		panic(err)
	}

	newUser := FirestoreUser{
		Level: getUserLevel(user.TotalExp + addedExp),
	}

	err = client.RunTransaction(ctx, func(ctx context.Context, tx *firestore.Transaction) error {
		return tx.Set(userRef.Ref, map[string]interface{}{
			"total_exp":              firestore.Increment(addedExp),
			"message_count":          firestore.Increment(1),
			"avatar_url":             user.AvatarUrl,
			"last_message_timestamp": time.Now().UTC().Format(DATETIME_FORMAT_EXAMPLE),
			"level":                  newUser.Level,
		}, firestore.MergeAll)
	})
	if err != nil {
		panic(err)
	}

	return newUser
}

// Send a private message to the user to inform him
func sendPrivateMessage(userId string, message string) {
	firestoreCtx := context.Background()
	client, err := pubsub.NewClient(firestoreCtx, "archy-f06ed")
	if err != nil {
		panic(err)
	}
	defer client.Close()

	topicClient := client.Topic("private_message_discord")

	pubsubData, err := json.Marshal(PubsubDataPrivateMessage{UserId: userId, Message: message})
	if err != nil {
		panic(err)
	}

	result := topicClient.Publish(firestoreCtx, &pubsub.Message{
		Data: []byte(pubsubData),
	})

	messageId, err := result.Get(firestoreCtx)
	if err != nil {
		panic(err)
	}

	log.Printf("Message send to user, messageId: " + messageId)
}

func getUserLevel(userTotalExp int) int {
	levels := []int{
		100,
		255,
		475,
		770,
		1150,
		1625,
		2205,
		2900,
		3720,
		4675,
		5775,
		7030,
		8450,
		10045,
		11825,
		13800,
		15980,
		18375,
		20995,
		23850,
		26950,
		30305,
		33925,
		37820,
		42000,
		46475,
		51255,
		56350,
		61770,
		67525,
		73625,
		80080,
		86900,
		94095,
		101675,
		109650,
		118030,
		126825,
		136045,
		145700,
		155800,
		166355,
		177375,
		188870,
		200850,
		213325,
		226305,
		239800,
		253820,
		268375,
		283475,
		299130,
		315350,
		332145,
		349525,
		367500,
		386080,
		405275,
		425095,
		445550,
		466650,
		488405,
		510825,
		533920,
		557700,
		582175,
		607355,
		633250,
		659870,
		687225,
		715325,
		744180,
		773800,
		804195,
		835375,
		867350,
		900130,
		933725,
		968145,
		1003400,
		1039500,
		1076455,
		1114275,
		1152970,
		1192550,
		1233025,
		1274405,
		1316700,
		1359920,
		1404075,
		1449175,
		1495230,
		1542250,
		1590245,
		1639225,
		1689200,
		1740180,
		1792175,
		1845195,
		1899250,
	}

	var level int

	for i, exp := range levels {
		if userTotalExp < exp {
			return i + 1
		}
	}

	return level
}

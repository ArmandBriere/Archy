package answer

import (
	"math/rand"
	"net/http"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

var possibleAnswers = []string{
	"It is certain",
	"Reply hazy, try again",
	"Don't count on it",
	"It is decidedly so",
	"Ask again later",
	"My reply is no",
	"Without a doubt",
	"Better not tell you now",
	"My sources say no",
	"Yes definitely",
	"Cannot predict now",
	"Outlook not so good",
	"You may rely on it",
	"Concentrate and ask again",
	"Very doubtful",
	"As I see it, yes",
	"Most likely",
	"Outlook good",
	"Yes",
	"Signs point to yes",
}

// init setup storage and firestore client.
func init() {
	functions.HTTP("Answer", Answer)
}

func Answer(w http.ResponseWriter, _ *http.Request) {
	index := rand.Intn(len(possibleAnswers))
	w.Write([]byte(possibleAnswers[index]))
}

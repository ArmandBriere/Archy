const express = require('express')
const fs = require('fs');
const lib = require('../index')
const nunjucks = require('nunjucks');

const app = express();
const path = require("path");

const router = express.Router();

app.set("templates", path.join(__dirname, "templates/"));

const payload = {
    username: "Hannibal119",
    avatar_url: "https://cdn.discordapp.com/avatars/135048445097410560/cf784bf15d1575d1feee5e35692dd3dc.webp?size=1024",
    rank: 33,
    level: 55,
    percent: 48,
}

async function execute() {

    let html = nunjucks.render(path.resolve(__dirname, '../templates/level.html'), {
        username: payload.username,
        avatar_url: payload.avatar_url,
        rank: payload.rank,
        level: payload.level,
        percent: payload.percent,
    });

    const imageBuffer = await lib.generateImage(html);
    fs.createWriteStream("test.png").write(imageBuffer);
}


router.get('/', (req, res) => {

    adjectives = [
        "Amazing",
        "Beautiful",
        "Breathtaking",
        "Delightful",
        "Excellent",
        "Exquisite",
        "Epic",
        "Magnificent",
        "Marvelous",
        "Glorious",
        "Gorgeous",
        "Ravishing",
        "Stunning",
        "Splendid",
        "Superb",
        "Wow",
        "Wonderful",
    ]

    let html = nunjucks.render(path.resolve(__dirname, '../templates/level.html'), {
        username: payload.username,
        adjectif: adjectives[Math.floor(Math.random() * adjectives.length)],
        avatar_url: payload.avatar_url,
        rank: payload.rank,
        level: payload.level,
        percent: payload.percent,
    });

    res.setHeader("Content-Type", "text/html")
    res.send(html);
});

app.use("/", router);
app.listen(process.env.port || 3000);

console.log(__dirname)

console.log("Running at Port 3000");
execute();

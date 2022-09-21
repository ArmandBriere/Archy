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
}

async function execute() {

    let html = nunjucks.render(path.resolve(__dirname, '../templates/welcome.html'), {
        username: payload.username,
        avatar_url: payload.avatar_url,
    });

    const imageBuffer = await lib.generateImage(html);
    fs.createWriteStream("test.png").write(imageBuffer);
}


router.get('/', (req, res) => {

    let html = nunjucks.render(path.resolve(__dirname, '../templates/welcome.html'), {
        username: payload.username,
        avatar_url: payload.avatar_url,
    });

    res.setHeader("Content-Type", "text/html")
    res.send(html);
});

app.use("/", router);
app.listen(process.env.port || 3000);

console.log(__dirname)

console.log("Running at Port 3000");
execute();

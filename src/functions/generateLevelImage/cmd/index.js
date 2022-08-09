const nunjucks = require('nunjucks');
const fs = require('fs');

const lib = require('../index')


async function execute() {
    payload = {
        username: "Hannibal119",
        avatar_url: "https://cdn.discordapp.com/avatars/135048445097410560/cf784bf15d1575d1feee5e35692dd3dc.webp?size=1024",
        rank: 33,
        level: 55,
        percent: 48,
    }

    let html = nunjucks.render('./templates/level.html', {
        username: payload.username,
        avatar_url: payload.avatar_url,
        rank: payload.rank,
        level: payload.level,
        percent: payload.percent,
    });

    const imageBuffer = await lib.generateImage(html);
    fs.createWriteStream("test.png"). write(imageBuffer);
}


execute();

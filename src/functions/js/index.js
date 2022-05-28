/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
const { Client, Intents } = require('discord.js');

exports.js = (req, res) => {
    // Create a new client instance
    const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

    // When the client is ready, run this code (only once)
    client.once("ready", () => {
        console.log("Ready!");
        reqChannelId = req.body.channel_id
        client.channels.fetch(reqChannelId).then(async (channel) => {
            message = await channel.send("Hi, i'm sending message from JS");
            message.react("❤")
            console.log("Done!");
            setTimeout((() => { client.destroy(); res.end() }), 100)
        });
    });

    // Login to Discord with your client's token
    client.login("DISCORD_TOKEN");
};
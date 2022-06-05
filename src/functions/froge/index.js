/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
const { Client, Intents } = require('discord.js');

exports.froge = (req, res) => {
    // Create a new client instance
    const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS] });

    // When the client is ready, run this code (only once)
    client.once("ready", () => {
        console.log("Ready!");
        reqChannelId = req.body.channel_id
        client.channels.fetch(reqChannelId).then(async (channel) => {
            // Get all emojis starting with "froge"
            froges = client.emojis.cache.filter(emoji => emoji.name.match("froge*"));
            froges = Array.from(froges);
            
            // Select a random one
            selectedFroge = froges[Math.floor(Math.random() * froges.length)];

            // Return that one
            message = await channel.send(`${selectedFroge[1]}`);
            console.log("Done!");
            setTimeout((() => { client.destroy(); res.end() }), 100)
        });
    });

    // Login to Discord with your client's token
    client.login(process.env.DISCORD_TOKEN);

};

// import {} from '../apiBot/Bot'
import { Client, GatewayIntentBits, TextChannel } from 'discord.js';
import { Payload } from '../types/Payload';

function isTextCh(arg: any): arg is TextChannel { return arg && arg.type && arg.type === "text"; }

const handleDiscordApi = async (token: string, pollMsgId: string, payload: Payload) => {
  const client: Client = new Client({
      intents: [GatewayIntentBits.Guilds]
  })

  client.login(token)

  const channel = await client.channels.fetch(payload.channelId)
  
  if (channel && isTextCh(channel)) {
    const votes: Array<[string, number]> = []
    const messages = await channel.messages.fetch({ limit: 5, cache: false, around: pollMsgId })
    const pollMsg = messages.filter(m => m.author.id == client!.user!.id).first()
    
    pollMsg?.reactions.cache.each(
      r => votes.push([r.toString(), r.count])
    )

    const voteCountText = votes
      .map(([reaction, count]) => `${reaction}: ${count} votes`)
      .join("\n")

    return voteCountText
  } else {
    return "No votes or poll found."
  }
}

export {
  handleDiscordApi,
}

import { Request, Response } from 'express'
import { handlePrompt } from './handlers/promptHandler'
import { parseToPrompt } from './parsers/PayloadParser'
import { dtoToPayload, Payload, PayloadDto } from './types/Payload'
import { promptTypes } from './types/PromptType'

import { handleDiscordApi } from './handlers/discordApiHandler'

/**
 * Responds to any HTTP request.
 *
 * @param _ HTTP request context.
 * @param res HTTP response context.
 */
exports.poll = (request: Request, res: Response) => {
  if (request.body === null || request.body === undefined) {
    res.status(200).send('Il vous manque des paramètres, le bon format est : `!poll &lt;question&gt;`')
    return
  }

  let payload: Payload
  try {
    const dto = request.body as PayloadDto
    payload = dtoToPayload(dto)
  } catch {
    res.status(200).send('Erreur de lecture, le bon format de la commande est : `!poll &lt;question&gt;')
    return
  }

  const prompt = parseToPrompt(payload)
  if (prompt.type === promptTypes.invalid) {
    res.status(200).send(prompt.message)
    return
  }

  const result = handlePrompt(prompt)

  res.status(200).send(`${payload.messageId}\n${result}`)
}

/**
 * Responds to any HTTP request.
 *
 * @param _ HTTP request context.
 * @param res HTTP response context.
 */
exports.pollCheck = (request: Request, res: Response) => {
  if (request.body === null || request.body === undefined) {
    res.status(200).send('Il vous manque des paramètres, le bon format est : `!poll &lt;question&gt;`')
    return
  }

  let payload: Payload
  try {
    const dto = request.body as PayloadDto
    payload = dtoToPayload(dto)
  } catch {
    res.status(200).send('Erreur de lecture, le bon format de la commande est : `!poll &lt;question&gt;')
    return
  }

  // const prompt = parseToDiscordApiCommand(payload)
  // if (prompt.type === promptTypes.invalid) {
  //   res.status(400).send(prompt.message)
  //   return
  // }
  if (!payload.params || !payload.params[0]) {
    return
  }
  const pollMsgId = payload.params[0]

  const TOKEN = process.env["DISCORD_TOKEN"]
  if (!TOKEN) {
    res.status(200).send("Bad token")
    return
  }

  handleDiscordApi(TOKEN, pollMsgId, payload)
    .then(result => res.status(200).send(`${payload.messageId}\n${result}`))
    .catch(e => res.status(200).send(e.message))
}

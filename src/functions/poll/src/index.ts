import { Request, Response } from 'express'
import { handlePrompt } from './handlers/promptHandler'
import { parseToPrompt } from './parsers/PayloadParser'
import { dtoToPayload, Payload, PayloadDto } from './types/Payload'
import { promptTypes } from './types/PromptType'

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

  res.status(200).send(result)
};

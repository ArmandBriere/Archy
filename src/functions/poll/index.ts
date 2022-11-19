import { Request, Response } from 'express'
import { dtoToPayload, Payload, PayloadDto } from './types/Payload';
import { yesNoUseCase } from './useCases/yesNoUseCase';

/**
 * Responds to any HTTP request.
 *
 * @param _ HTTP request context.
 * @param res HTTP response context.
 */
exports.js = (request: Request, res: Response) => {
  if (request.body === null || request.body === undefined) {
    res.status(400).send('Il vous manque des paramètres, le bon format est : `!poll &lt;question&gt;`')
    return
  }

  let payload: Payload
  try {
    const dto = request.body as PayloadDto
    payload = dtoToPayload(dto)
  } catch {
    res.status(400).send('Erreur de lecture, le bon format de la commande est : `!poll &lt;question&gt;')
    return
  }

  const result = yesNoUseCase(payload)

  res.status(200).send(result)
};

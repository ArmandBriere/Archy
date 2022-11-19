import { Payload } from '../Payload'
import { promptTypes } from '../PromptType'
import { createInvalidPrompt, InvalidPrompt } from './InvalidPrompt'

export type MultipleChoicesPrompt = {
  type: typeof promptTypes.multiple,
  prompt: string,
  choices: string[],
}

export const multipleCondition = (payload: Payload): boolean => {
  return payload.params.length > 1
}

export const readMultiple = (payload: Payload): MultipleChoicesPrompt | InvalidPrompt => {
  const prompt = payload.params[0] ?? null
  if (prompt === null) return createInvalidPrompt('Mauvais format : `!poll &lt;question&gt; [...choix]`')

  const choices = payload.params.slice(1)

  return {
    type: promptTypes.multiple,
    prompt,
    choices,
  }
}

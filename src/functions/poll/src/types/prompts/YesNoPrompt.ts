import { Payload } from '../Payload'
import { promptTypes } from '../PromptType'
import { createInvalidPrompt, InvalidPrompt } from './InvalidPrompt'

export type YesNoPrompt = {
  type: typeof promptTypes.yesNo,
  prompt: string,
}

export const yesNoCondition = (payload: Payload): boolean => {
  return payload.params.length === 1
}

export const readYesNoPrompt = (payload: Payload): YesNoPrompt | InvalidPrompt => {
  const prompt = payload.params[0] ?? null
  if (prompt === null) return createInvalidPrompt('Mauvais format : `!poll &lt;question&gt;`')

  return {
    type: promptTypes.yesNo,
    prompt,
  }
}

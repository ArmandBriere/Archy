import { promptify } from '../utils/promptify'
import { Payload } from '../types/Payload'
import { readYesNoPrompt } from '../types/YesNoPrompt'

const yesNoUseCase = (payload: Payload): string | null => {
  const prompt = readYesNoPrompt(payload)
  if (!prompt) return null

  const result = promptify(prompt.prompt)

  return result
}

export {
  yesNoUseCase,
}

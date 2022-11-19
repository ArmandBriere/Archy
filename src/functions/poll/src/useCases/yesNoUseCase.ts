import { promptifyYesNo } from '../utils/promptify'
import { YesNoPrompt } from '../types/prompts/YesNoPrompt'

const yesNoUseCase = (prompt: YesNoPrompt): string => {
  const result = promptifyYesNo(prompt.prompt)

  return result
}

export {
  yesNoUseCase,
}

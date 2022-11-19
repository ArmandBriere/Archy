import { MultipleChoicesPrompt } from '../types/prompts/MultipleChoicesPrompt'
import { labelize } from '../utils/labelize'
import { promptifyMultiple } from '../utils/promptify'

const multipleUseCase = (prompt: MultipleChoicesPrompt): string => {
  const choices = labelize(prompt.choices)
  const result = promptifyMultiple(prompt.prompt, choices)
  return result
}

export {
  multipleUseCase,
}

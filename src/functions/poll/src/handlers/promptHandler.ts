import { Prompt } from '../types/Prompt'
import { InvalidPrompt } from '../types/prompts/InvalidPrompt'
import { promptTypes } from '../types/PromptType'
import { multipleUseCase } from '../useCases/multipleUseCase'
import { yesNoUseCase } from '../useCases/yesNoUseCase'

const handlePrompt = (prompt: Exclude<Prompt, InvalidPrompt>): string => {
  switch (prompt.type) {
    case promptTypes.yesNo:
      return yesNoUseCase(prompt)

    case promptTypes.multiple:
      return multipleUseCase(prompt)

    default:
      return 'Erreur inconnue de la commande `!poll`'
  }
}

export {
  handlePrompt,
}

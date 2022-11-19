import { Payload } from '../types/Payload'
import { Prompt } from '../types/Prompt'
import { createInvalidPrompt } from '../types/prompts/InvalidPrompt'
import { multipleCondition, readMultiple } from '../types/prompts/MultipleChoicesPrompt'
import { yesNoCondition, readYesNoPrompt } from '../types/prompts/YesNoPrompt'

const parseToPrompt = (payload: Payload): Prompt => {
  if (yesNoCondition(payload)) {
    return readYesNoPrompt(payload)
  } else if (multipleCondition(payload)) {
    return readMultiple(payload)
  } else {
    return createInvalidPrompt('Commande invalide, le bon format est : `!poll &lt;question&gt; [...choix]`')
  }
}

export {
  parseToPrompt,
}

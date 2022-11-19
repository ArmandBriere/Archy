import { InvalidPrompt } from './prompts/InvalidPrompt'
import { MultipleChoicesPrompt } from './prompts/MultipleChoicesPrompt'
import { YesNoPrompt } from './prompts/YesNoPrompt'

export type Prompt =
  | YesNoPrompt
  | MultipleChoicesPrompt
  | InvalidPrompt

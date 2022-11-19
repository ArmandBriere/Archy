import { promptTypes } from '../PromptType'

export type InvalidPrompt = {
  type: typeof promptTypes.invalid,
  message: string,
}

export const createInvalidPrompt = (message: string): InvalidPrompt => ({
  type: promptTypes.invalid,
  message,
})

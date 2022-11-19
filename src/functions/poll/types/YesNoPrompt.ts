import { Payload } from "./Payload"

export type YesNoPrompt = {
  prompt: string,
}

export const readYesNoPrompt = (payload: Payload): YesNoPrompt | null => {
  const prompt = payload.params[0] ?? null
  if (prompt === null) return null

  return {
    prompt,
  }
}

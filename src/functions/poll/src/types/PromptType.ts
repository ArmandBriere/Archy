export const promptTypes = {
  invalid: 'invalid',
  yesNo: 'yesNo',
  multiple: 'multiple',
} as const

export type PromptType = typeof promptTypes[keyof typeof promptTypes]

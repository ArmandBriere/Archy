const yesOption = `✅ : Oui`
const noOption = `❌ : Non`

const promptifyYesNo = (prompt: string): string => {
  return `${prompt}\n${yesOption}\n${noOption}`
}

const promptifyMultiple = (prompt: string, choices: string[]): string => {
  return `${prompt}\n${choices.join('\n')}`
}

export {
  promptifyYesNo,
  promptifyMultiple,
}

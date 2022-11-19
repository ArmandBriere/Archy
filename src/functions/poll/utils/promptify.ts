const yesOption = `✅ : Oui`
const noOption = `❌ : Non`

const promptify = (prompt: string): string => {
  return `${prompt}\n${yesOption}\n${noOption}`
}

export {
  promptify,
}

const baseNumberCode = 0x0030
const escapeCode1 = 0xFE0F
const escapeCode2 = 0x20E3

const labelize = (choices: string[]): string[] => {
  const result: string[] = []

  let nextPrefixCode = baseNumberCode
  for (const choice of choices) {
    const label = String.fromCharCode(nextPrefixCode++, escapeCode1, escapeCode2)
    const labelized = `${label}: ${choice}`
    result.push(labelized)
  }

  return result
}

export {
  labelize,
}

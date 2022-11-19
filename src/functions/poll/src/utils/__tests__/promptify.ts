import { describe, it, expect } from '@jest/globals'
import { promptify } from '../promptify'

describe('promptify', () => {
  it('should turn the user\'s prompt into a proper poll prompt', () => {
    const expected = 'Do you like coffee?\n✅ : Oui\n❌ : Non'

    const prompt = 'Do you like coffee?'
    
    const result = promptify(prompt)

    expect(result).toBe(expected)
  })
})

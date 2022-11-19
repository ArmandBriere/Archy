import { describe, it, expect } from '@jest/globals'
import { promptifyMultiple, promptifyYesNo } from '../promptify'

describe('promptify', () => {
  describe('promptifyYesNo', () => {
    it('should turn the user\'s prompt into a proper poll prompt', () => {
      const expected = 'Do you like coffee?\n✅ : Oui\n❌ : Non'

      const prompt = 'Do you like coffee?'
      
      const result = promptifyYesNo(prompt)

      expect(result).toBe(expected)
    })
  })

  describe('promptifyMultiple', () => {
    it('should turn the user\'s prompt and choices into a proper poll prompt', () => {
      const expected = 'Do you like coffee?\nYes\nNo\nMaybe'

      const prompt = 'Do you like coffee?'

      const choices = [
        'Yes',
        'No',
        'Maybe',
      ]
      
      const result = promptifyMultiple(prompt, choices)

      expect(result).toBe(expected)
    })
  })
})

import { describe, expect, it } from '@jest/globals'
import { labelize } from '../labelize'

describe('labelize', () => {
  describe('labelize', () => {
    it('should add a number at the start of each choice', () => {
      const expected = [
        '0️⃣: Yes',
        '1️⃣: No',
        '2️⃣: Maybe',
      ]

      const choices = [
        'Yes',
        'No',
        'Maybe',
      ]

      const result = labelize(choices)

      expect(result).toEqual(expected)
    })
  })
})

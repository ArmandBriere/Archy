import { describe, expect, it } from '@jest/globals'
import { dtoToPayload, PayloadDto } from '../Payload'

describe('Payload', () => {
  describe('dtoToPayload', () => {
    it('should parse the params and split them correctly into quoted segments', () => {
      const expected = [
        'Do you like coffee?',
        'Yes',
        'No',
        'Maybe',
      ]

      const params = [
        '"Do',
        'you',
        'like',
        'coffee?"',
        '"Yes"',
        '"No"',
        '"Maybe"',
      ]

      const dto: PayloadDto = {
        params,
      }

      const result = dtoToPayload(dto)

      expect(result.params).toEqual(expected)
    })
  })
})

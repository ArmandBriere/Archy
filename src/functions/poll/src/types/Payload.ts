export type PayloadDto = {
  server_id?: string,
  server_name?: string,
  user_id?: string,
  mentions?: string[],
  params?: string[],
}

export type Payload = {
  serverId: string,
  serverName: string,
  userId: string,
  mentions: string[],
  params: string[],
}

const delimiter = '"'

const dtoToParams = (dto: string[]): string[] => {
  const results: string[] = []

  let opened = false
  let segments: string[] = []
  for (const part of dto) {
    let remaining = part
    while (remaining !== '') {
      const indexOfDelimiter = remaining.indexOf(delimiter)

      if (indexOfDelimiter < 0) {
        segments.push(remaining)
        remaining = ''
      } else if (opened) {
        // Close the quotation and flush to the results.
        const segment = remaining.substring(0, indexOfDelimiter)
        remaining = remaining.substring(indexOfDelimiter + 1)

        segments.push(segment)
        results.push(segments.join(' '))

        opened = false
        segments = []
      } else {
        // Start to process segments.
        remaining = remaining.substring(indexOfDelimiter + 1)
        opened = true
      }
    }
  }

  return results
}

export const dtoToPayload = (dto: PayloadDto): Payload => ({
  serverId: dto.server_id ?? '',
  serverName: dto.server_name ?? '',
  userId: dto.user_id ?? '',
  mentions: dto.mentions ?? [],
  params: dtoToParams(dto.params ?? []),
})

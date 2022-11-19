export type PayloadDto = {
  server_id: string,
  server_name: string,
  user_id: string,
  mentions: string[],
  params: string[],
}

export type Payload = {
  serverId: string,
  serverName: string,
  userId: string,
  mentions: string[],
  params: string[],
}

export const dtoToPayload = (dto: PayloadDto): Payload => ({
  serverId: dto.server_id ?? '',
  serverName: dto.server_name ?? '',
  userId: dto.user_id ?? '',
  mentions: dto.mentions ?? [],
  params: dto.params ?? [],
})

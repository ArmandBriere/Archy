
export interface DiscordUserToken {
  "access_token": string,
  "token_type": string,
  "expires_in": number,
  "scope": string
}

export interface DiscordUser {
  "id": string,
  "username": string,
  "avatar": string,
  "discriminator": string,
}
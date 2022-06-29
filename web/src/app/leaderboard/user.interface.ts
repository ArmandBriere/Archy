
export interface User {
    username: string,
    rank: number,
    level: number,
    total_exp: number,
    exp_toward_next_level: number,
    message_count: number,
    avatar_url: string | undefined
}
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HomePageService {

  API_ENDPOINT = 'https://discord.com/api/v10'
  CLIENT_ID = '964693548396068916'
  CLIENT_SECRET = 'CLIENT_SECRET'
  REDIRECT_URI = 'http://localhost:4200/'
  constructor(
    private httpClient: HttpClient,
  ) { }

  getToken(userCode: string): Observable<any> {

    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    const params = new URLSearchParams();
    params.append('client_id', this.CLIENT_ID);
    params.append('client_secret', this.CLIENT_SECRET);
    params.append('grant_type', 'authorization_code');
    params.append('code', userCode);
    params.append('redirect_uri', this.REDIRECT_URI);
    return this.httpClient.post(`${this.API_ENDPOINT}/oauth2/token`, params, { headers })
  }

  getUserInfo(accessToken: string) {
    const token = `Bearer ${accessToken}`
    return this.httpClient.get("https://discordapp.com/api/users/@me", { headers: { Authorization: token } })
  }

}

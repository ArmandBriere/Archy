import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {

  }

  oauth(): void {
    const oauthUrlPrefix = "https://discord.com/oauth2/authorize?response_type=code&scope=identify%20guilds.join&"
    const clientId = '964693548396068916'
    const redirectUrl = 'http://localhost:4200/'

    window.location.href = `${oauthUrlPrefix}client_id=${clientId}&redirect_uri=${redirectUrl}`
  }
}

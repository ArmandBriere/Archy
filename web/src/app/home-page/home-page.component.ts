import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DiscordUser, DiscordUserToken } from './discord.interface';
import { HomePageService } from './home-page.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {

  userCode!: string | null;
  userData!: DiscordUser | any;

  constructor(private homePageService: HomePageService,
    private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.userCode = params['code'];

      if (this.userCode !== null && this.userCode !== "") {
        this.homePageService.getToken(this.userCode).subscribe((data: DiscordUserToken) => {
          localStorage.setItem('discordToken', JSON.stringify(data));
          this.homePageService.getUserInfo(data['access_token']).subscribe((userData) => {
            this.userData = userData;
          })
        })
      }

      const localStorageData = localStorage.getItem('discordToken')
      if (localStorageData !== null && localStorageData !== "") {
        const data = JSON.parse(localStorageData);
        this.homePageService.getUserInfo(data['access_token']).subscribe((userData) => {
          this.userData = userData;
        })
      }
    }
    );
  }

}

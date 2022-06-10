import { Component, OnInit } from '@angular/core';
import { LeaderboardService } from './leaderboard.service';
import { User } from './user.interface';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.scss']
})
export class LeaderboardComponent implements OnInit {

  users: User[] | undefined;
  
  constructor(private leaderboardService: LeaderboardService) { }

  ngOnInit(): void {
    let data = this.leaderboardService.getUsers().subscribe(data => {
      if (data) {
        this.users = data;
      }
      console.log(data);
    });
  }

}

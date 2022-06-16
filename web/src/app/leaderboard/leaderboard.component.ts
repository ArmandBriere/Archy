import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LeaderboardService } from './leaderboard.service';
import { User } from './user.interface';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.scss']
})
export class LeaderboardComponent implements OnInit {

  users: User[] | undefined;
  serverId: string | null | undefined;

  constructor(private leaderboardService: LeaderboardService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.serverId = this.route.snapshot.paramMap.get('id');

    if (this.serverId) {
      this.leaderboardService.getUsers(this.serverId).subscribe(data => {
        if (data) {
          this.users = data;
        }
      });
    }
  }

}

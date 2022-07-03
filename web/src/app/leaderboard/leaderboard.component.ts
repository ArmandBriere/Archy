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
          this.users.forEach(user => {
            let level_exp_needed = 5 * (user.level ** 2) + (50 * user.level) + 100
            user.progress = user.exp_toward_next_level / level_exp_needed * 100

          });
        }
      });
    }
  }

}

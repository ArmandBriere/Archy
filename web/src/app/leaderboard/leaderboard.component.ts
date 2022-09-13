import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LeaderboardService } from './leaderboard.service';
import { User } from '@interface/user.interface';

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

            if (user.progress === 100) {
              user.progress = 99;
            }

          });
        }
      });
    }
  }

}


import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatWithK'
})
export class FormatWithKPipe implements PipeTransform {
  transform(num: number): string | number {
    return Math.abs(num) > 999 ? Math.sign(num) * (Number((Math.abs(num) / 1000).toFixed(1))) + 'K' : Math.sign(num) * Math.abs(num)
  }
}

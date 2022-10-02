import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';

const routes: Routes = [
  { path: '', component: HomePageComponent },
  {
    path: 'servers',
    loadChildren: () =>
      import('./server/server.module').then(
        (m) => m.ServerModule
      ),
  },
  { path: 'leaderboard/:id', component: LeaderboardComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

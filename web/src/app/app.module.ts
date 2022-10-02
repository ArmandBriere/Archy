import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SharedModule } from './shared/shared.module';
import { HomePageComponent } from './home-page/home-page.component';
import { FormatWithKPipe, LeaderboardComponent } from './leaderboard/leaderboard.component';
import { AngularFirestoreModule } from '@angular/fire/compat/firestore';

import { environment } from 'src/environments/environment';
import { provideAppCheck } from '@angular/fire/app-check';
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';
import { provideFirebaseApp } from '@angular/fire/app';
import { getApp, initializeApp } from 'firebase/app';
import { AngularFireModule } from '@angular/fire/compat';
import { ContributorComponent } from './contributor/contributor.component';


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    LeaderboardComponent,
    FormatWithKPipe,
    ContributorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    SharedModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFirestoreModule,
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAppCheck(() => {
      const provider = new ReCaptchaV3Provider(environment.captcha);
      return initializeAppCheck(getApp(), {
        provider,
        isTokenAutoRefreshEnabled: true,
      });
    }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule,APP_INITIALIZER,LOCALE_ID } from '@angular/core';
import { BrowserModule, Title } from '@angular/platform-browser';

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

import { I18NextModule, ITranslationService, I18NEXT_SERVICE, I18NextTitle, defaultInterpolationFormat } from 'angular-i18next';

import LanguageDetector from 'i18next-browser-languagedetector'
import I18NextXhrBackend from 'i18next-xhr-backend';


export function appInit(i18next: ITranslationService) {
  return () => 
  i18next
  .use<any>(LanguageDetector)
  .use(I18NextXhrBackend)
  .init({
      //whitelist: ['en', 'gr'],
      fallbackLng: 'en',
      debug: true,
      returnEmptyString: false,
      ns: [
        'translation',
        'validation',
        'error',
      ],
      interpolation: {
        format: I18NextModule.interpolationFormat(defaultInterpolationFormat)
      },
      backend: {
        loadPath: 'assets/locales/{{lng}}.{{ns}}.json',
      },
      detection: {
        // order and from where user language should be detected
        order: ['querystring', 'cookie'],
        // keys or params to lookup language from
        lookupCookie: 'lang',
        lookupQuerystring: 'lng',
        // cache user language on
        caches: ['localStorage', 'cookie'],
        // optional expire and domain for set cookie
        cookieMinutes: 10080, // 7 days
      }
    });
}

export function localeIdFactory(i18next: ITranslationService)  {
  return i18next.language;
}

export const I18N_PROVIDERS = [
  {
    provide: APP_INITIALIZER,
    useFactory: appInit,
    deps: [I18NEXT_SERVICE],
    multi: true
  },
  {
    provide: Title,
    useClass: I18NextTitle
  },
  {
    provide: LOCALE_ID,
    deps: [I18NEXT_SERVICE],
    useFactory: localeIdFactory
  }];


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    LeaderboardComponent,
    FormatWithKPipe,
    ContributorComponent
  ],
  imports: [
    I18NextModule.forRoot(),
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
  providers: [I18N_PROVIDERS],
  bootstrap: [AppComponent]
})
export class AppModule { }

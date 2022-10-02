import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServerComponent } from './server.component';
import { ServerRoutingModule } from './server-routing.module';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [
    ServerComponent
  ],
  imports: [
    CommonModule,
    ServerRoutingModule,
    SharedModule
  ]
})
export class ServerModule { }

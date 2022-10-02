import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { ServerInterface } from '@interface/server.interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServerService {

  constructor(private db: AngularFirestore) { }

  getServers(): Observable<any[]> {
    return this.db.collection("serverList").valueChanges();
  }
}

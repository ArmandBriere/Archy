import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { User } from '@interface/user.interface';

@Injectable({
  providedIn: 'root'
})
export class LeaderboardService {

  constructor(private db: AngularFirestore) { }

  getUsers(serverId: string) {
    return this.db.collection('servers').doc(serverId).collection<User>('users', ref => ref.orderBy('total_exp', 'desc').limit(50)).valueChanges();
  }
}

import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { User } from './user.interface';

@Injectable({
  providedIn: 'root'
})
export class LeaderboardService {

  constructor(private db: AngularFirestore) { }

  /**
   * Get all boards owned by current user
   */
  getUsers(serverId: string) {
    return this.db.collection('servers').doc(serverId).collection<User>('users', ref => ref.orderBy('total_exp', "desc")).valueChanges();
  }
}

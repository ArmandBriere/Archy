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
  getUsers() {
    return this.db.collection<User>('users', ref => ref.orderBy('total_exp', "desc")).valueChanges();
  }
}

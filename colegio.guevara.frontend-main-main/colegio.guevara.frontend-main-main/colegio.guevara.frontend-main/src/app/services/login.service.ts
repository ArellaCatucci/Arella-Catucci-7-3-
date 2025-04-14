import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private _datos = ['dato1', 'dato2', 'dato3', 'dato4'];

  get datos(){
    return [...this._datos]
  }

  constructor() { }
}

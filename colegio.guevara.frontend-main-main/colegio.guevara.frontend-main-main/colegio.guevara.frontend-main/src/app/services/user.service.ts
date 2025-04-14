import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private _usuarioConectado: string = '';

  set usuarioConectado(usuario: string) {
    this._usuarioConectado = usuario;
  }

  get usuarioConectado(): string {
    return this._usuarioConectado;
  }

  get isConnected(): boolean {
    return this._usuarioConectado !== '';
  }
  




}

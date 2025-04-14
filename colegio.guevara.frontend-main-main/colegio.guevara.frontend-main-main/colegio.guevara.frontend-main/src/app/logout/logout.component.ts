import { Component } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent {

  constructor(private userService: UserService) {
    
    localStorage.removeItem('usuarioConectado');
    this.userService.usuarioConectado = '';
    console.log('Logout')
  }

}

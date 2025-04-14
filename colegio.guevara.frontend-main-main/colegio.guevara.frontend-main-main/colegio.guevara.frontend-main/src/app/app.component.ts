import { Component } from '@angular/core';
import { LoginService } from './services/login.service';
import { UserService } from './services/user.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'tvworld v1.0';
  
  counterRecibido:number = 0;
  usuarioConectado: any;

  sidebarActive = false;

  toggleSidebar() {
    this.sidebarActive = !this.sidebarActive;
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
      sidebar.classList.toggle('active', this.sidebarActive);
    }
  }

  procesarCounter(count: number) {
    this.counterRecibido = count;

  }

  get isConnected() {
    return this.userService.isConnected;
  }

  get datos() {
    return this.loginService.datos;
    
  }
  constructor(
    private loginService: LoginService,
    private userService: UserService
  ) {

  }

}

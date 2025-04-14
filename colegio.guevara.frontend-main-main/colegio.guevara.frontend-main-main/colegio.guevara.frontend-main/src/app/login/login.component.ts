import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { MediafilesService } from '../services/media_files.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
  username : string = '';
  password : string = '';
  usuarioConectado : string ='';
  usuarioURL: string ='';
  usuarioRol: string = '';
  errorMessage: string = '';  // Mensaje de error a mostrar
  
  

  constructor(private authService: AuthService, private router: Router, private userService: UserService) {}
  

  login() {
    this.errorMessage = ''; // Resetear error antes de intentar loguearse

    this.authService.login(this.username, this.password).subscribe({
      next: (salida) => {
        //console.log(salida);
        localStorage.setItem('usuarioConectado', this.username); // Almacena el usuario
        this.userService.usuarioConectado = this.username; // Almacena el usuario
        this.usuarioURL = salida.url;
        this.usuarioRol = salida.rol;

        localStorage.setItem('usuarioURL', this.usuarioURL);
        localStorage.setItem('usuarioRol', this.usuarioRol);
        this.router.navigate(['/home']); // Navega sin depender del estado
      },
        error: (error) => {
          console.error('Login failed:', error);

          if (error.status === 401) {
            this.errorMessage = 'Usuario o contraseña incorrectos.';
          } else if (error.status === 0) {
            this.errorMessage = 'El servicio no está disponible. Inténtelo más tarde.';
          } else {
            this.errorMessage = 'Ocurrió un error inesperado. Inténtelo nuevamente.';
          };
        }
    });
  }
  

}

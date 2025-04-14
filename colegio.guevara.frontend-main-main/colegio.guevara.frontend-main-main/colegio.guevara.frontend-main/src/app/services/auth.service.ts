import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environments';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  //private baseUrl = 'http://localhost:8000';             // Felipe
  //private baseUrl = 'http://localhost/tvworld/public/api'; // Marcos
  private baseUrl = environment.apiUrl;
  

  usuarioConectado:string = ''; 
  url:string ='';

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    const url = `${this.baseUrl}/login/`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = { username, password };
    

    const salida = this.http.post(url, body, { headers });
    console.log(salida);
    this.usuarioConectado = username;
    //this.url = 

    return salida;
  }
}

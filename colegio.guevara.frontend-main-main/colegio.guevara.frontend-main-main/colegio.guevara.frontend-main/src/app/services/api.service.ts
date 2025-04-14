import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environments';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl; // Usamos la variable de ambiente

  constructor(private http: HttpClient) {}

  getData() {
    return this.http.get(`${this.apiUrl}/datos`);
  }
}

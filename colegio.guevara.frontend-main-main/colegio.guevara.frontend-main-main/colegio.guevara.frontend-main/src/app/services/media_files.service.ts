import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MediaItem, Comment } from '../models/media.model';
import { environment } from 'src/environments/environments';

@Injectable({
  providedIn: 'root'
})
export class MediafilesService {

  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  list(usuarioConectado:string): Observable<any> {
    const url = `${this.baseUrl}/media_files_owner/${usuarioConectado}`;
    console.log(url);
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
   
    const salida = this.http.get(url,{ headers });
    console.log(salida);
    
    return salida;
  }


  // Método para subir un nuevo elemento multimedia
  addMedia(media: MediaItem): Observable<MediaItem> {
    const url = `${this.baseUrl}/media_files`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    return this.http.post<MediaItem>(url, media, { headers });
  }

  
  // Método para subir un nuevo comentario de un elemento multimedia
  addComment(comment: Comment): Observable<Comment> {
    const url = `${this.baseUrl}/media_files_comments`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    

    return this.http.post<Comment>(url, comment, { headers });
  }




  // Subir archivo al backend
  uploadFile(file: File): Observable<any> {
    const url = `${this.baseUrl}/uploadFile`;
    const formData = new FormData();
    formData.append('file', file); 

    return this.http.post<any>(`${url}`, formData);
  }

}

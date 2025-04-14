import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { MediafilesService} from '../services/media_files.service';
import { MediaItem } from '../models/media.model';



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {
  mediaItems: MediaItem[] = []


//   mediaItems: MediaItem[] = [
//     {id:1, title: 'Imagen 1.3', owner: 'Felipe', type: 'image', src: 'https://via.placeholder.com/300', comments:[]},
//     {id:2, title: 'Imagen 1.1', owner: 'Marcos', type: 'image', src: 'https://via.placeholder.com/300', comments:[] },
//     {id:3, title: 'Video 1', owner: 'JUan', type: 'video', src: 'https://www.w3schools.com/html/mov_bbb.mp4', comments:[] },
//     {id:4, title: 'Imagen 2',owner: 'Pedro', type: 'image', src: 'https://via.placeholder.com/400', comments:[]},
//     {id:5, title: 'Video 2', owner: 'Felipe', type: 'video', src: 'https://www.w3schools.com/html/movie.mp4', comments:[]},
//     {id:6, title: 'Luna', owner: 'Felipe', type: 'image', src: 'https://www.researchgate.net/profile/Gareth-Roberts-3/publication/251839685/figure/fig3/AS:652228557803529@1532514814266/a-A-SEVIRI-400-x-400-pixel-scene-of-southern-Africa-September-4-th-1212pm.png', comments:[]}
//   ];


  
//   mediaItems1: MediaItem[]  = [
//   {
//     id:1,
//     title: 'Imagen de paisaje',
//     owner: 'Juan Pérez',
//     type: 'image',
//     src: 'https://www.muyinteresante.com/wp-content/uploads/sites/5/2023/08/01/64c8a20035395.jpeg',
//     comments: [
//       {
//         user: { name: 'Carlos Díaz', photo: 'https://st4.depositphotos.com/1049680/19973/i/450/depositphotos_199737222-stock-photo-handsome-middle-age-man-happy.jpg' },
//         text: 'Hermoso paisaje, ¡me encanta!',
//         date: new Date()
//       },
//       {
//         user: { name: 'Ana Gómez', photo: 'https://st2.depositphotos.com/1715570/6792/i/950/depositphotos_67922675-stock-photo-beautiful-older-woman-smiling-with.jpg' },
//         text: 'Impresionante vista.',
//         date: new Date()
//       }
//     ]
//   },
//   {
//     id:2,
//     title: 'Video de la naturaleza',
//     owner: 'María López',
//     type: 'video',
//     src: 'https://www.w3schools.com/html/mov_bbb.mp4',
//     comments: [
//       {
//         user: { name: 'Luis García', photo: 'https://via.placeholder.com/50' },
//         text: 'Este video es fascinante.',
//         date: new Date()
//       }
//     ]
//   }
// ];


  usuarioConectado: string = '';
  usuarioConectadoOtro: string = '';
  usuarioURL: string = '';
  usuarioRol: string = 'alumno';
  

  constructor(private router: Router, private userService: UserService, private mediaFilesService: MediafilesService ) {}

  ngOnInit() {
    
    //this.usuarioConectado = this.userService.usuarioConectado || 'Usuario no identificado';
    this.usuarioConectado = localStorage.getItem('usuarioConectado') || 'Usuario no identificado';
    if (this.usuarioConectado === 'Usuario no identificado') {
      this.router.navigate(['/login']);
    }
    else{  
      this.usuarioURL = localStorage.getItem('usuarioURL') || '';
      this.usuarioRol = localStorage.getItem('usuarioRol') || '';
      this.mediaFilesService.list(this.usuarioConectado).subscribe({
      next: (resultado) => {
        this.mediaItems = resultado; // Asigna el resultado a this.salida
        console.log('Media Files:', this.mediaItems);
      },
      error: (error) => console.error('Error obteniendo media files:', error)
    });}
    
  }
  
}

//como debagir por que no aparecen 
import { Component, Input } from '@angular/core';
import { MediaItem, Comment } from 'src/app/models/media.model';
import { MediafilesService } from 'src/app/services/media_files.service';

@Component({
  selector: 'app-media-card',
  templateUrl: './media-card.component.html',
  styleUrls: ['./media-card.component.css']
})

export class MediaCardComponent {

  @Input() media!: MediaItem;
  @Input() usuarioConectado:string = '';
  @Input() usuarioURL:string ='';
  
  playVideo(event: Event): void {
    const video = event.target as HTMLVideoElement;
    video.play();
  }
  
  constructor(private mediafilesService: MediafilesService) {}

  pauseVideo(event: Event): void {
    const video = event.target as HTMLVideoElement;
    video.pause();
  }

  newComment: string = ''; // Para almacenar el comentario actual del formulario

  addComment(): void {
    if (this.newComment.trim()) {
      const newComment = {
        uid_media : this.media.uid_media,
        user: {
          name: this.usuarioConectado, // Usuario conectado
          photo: this.usuarioURL
        },
        text: this.newComment,
        date: new Date()
      };

      this.mediafilesService.addComment(newComment).subscribe((savedComment: Comment)=> {
        this.media.comments.push(newComment);
        this.newComment = ''; // Limpia el formulario
      });

    }
  }

}

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MediaItem } from 'src/app/models/media.model';
import { MediafilesService } from 'src/app/services/media_files.service';

@Component({
  selector: 'app-media-gallery',
  templateUrl: './media-gallery.component.html',
  styleUrls: ['./media-gallery.component.css']
})
export class MediaGalleryComponent implements OnChanges{

  @Input() mediaItems: MediaItem[] = [];
  @Input() usuarioConectado:string = '';
  @Input() usuarioURL:string ='';
  @Input() usuarioRol:string ='';

  visibles: boolean[] = [];  // Controla qué tarjetas son visibles

  constructor(private mediafilesService: MediafilesService) {}

  ngOnInit() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => video.autoplay = false);
    console.log (this.usuarioURL);
    
  }
  
  ngOnChanges(changes: SimpleChanges) {
    if (changes['mediaItems'] && this.mediaItems.length > 0) {
      this.mostrarTarjetasConRetraso();
    }
  }
  


  mostrarTarjetasConRetraso() {

    this.visibles = new Array(this.mediaItems.length).fill(false);
   console.log('felipe adentro');
    this.mediaItems.forEach((_, index) => {
      console.log(`Mostrando tarjeta ${index} en ${index * 100} ms`);

      this.visibles[index] = true;
      setTimeout(() => {
        this.visibles[index] = true;
      }, index * 100); // Retrasa cada tarjeta 500ms
    });
  }

    // Reproduce el video al pasar el mouse
    playVideo(event: Event): void {
      const video = event.target as HTMLVideoElement;
      video.play();
    }
  
    // Pausa el video al salir el mouse
    pauseVideo(event: Event): void {
      const video = event.target as HTMLVideoElement;
      video.pause();
    }

    // Subir nuevas imagenes/videos
    newTitle: string = '';
    newFile: File | null = null;
    newType: 'image' | 'video' = 'image';

 


  
    handleFileInput(event: Event): void {
      console.log('Pasé por handleFileInput');
      const input = event.target as HTMLInputElement;
      if (input.files && input.files.length > 0) {
        this.newFile = input.files[0];
        
      }
    }
  
    // addMedia(): void {
    //   if (this.newFile && this.newTitle.trim()) {
    //     const newMedia = {
    //       uid_media: 0, //
    //       title: this.newTitle,
    //       owner: this.usuarioConectado,
    //       type: this.newType,
    //       src: URL.createObjectURL(this.newFile),
    //       comments: []
    //     };
    //     //this.mediaItems.push(newMedia);
    //     //this.resetForm();

    //     this.mediafilesService.addMedia(newMedia).subscribe((savedMedia: MediaItem)=> {
    //       this.mediaItems.push(newMedia);
    //       this.resetForm();
    //     });
    //   }
    // }

    addMediaUploadFile(): void {
      if (this.newFile && this.newTitle.trim()) {
  
        this.mediafilesService.uploadFile(this.newFile).subscribe((response: any) => {
          const newMedia: MediaItem = {
            uid_media: response.uid_media,  //- FMO: Agregado de nueva columna.
            title: this.newTitle,
            owner: this.usuarioConectado,
            type: this.newType,
            src: response.fileUrl, // URL del archivo guardado en el servidor
            created_at : new Date(),
            comments: []
          };
  
          this.mediafilesService.addMedia(newMedia).subscribe((savedMedia: MediaItem)=> {
            // Reasigna este valor, para que se pueda ver directamente en la web sin la necesidad de tener que cargar desde base de datos
            if (this.newFile instanceof File) {
              newMedia.src = URL.createObjectURL(this.newFile);
            }

            this.mediaItems.unshift(newMedia);
            this.resetForm();
          });
          
        });
      }
    }

    resetForm(): void {
      this.newTitle = '';
      this.newFile = null;
      this.newType = 'image';
    }
}

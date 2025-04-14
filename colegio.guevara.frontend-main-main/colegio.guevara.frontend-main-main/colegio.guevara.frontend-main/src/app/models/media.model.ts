export interface Comment {
    uid_media: string; // FMO Nueva columna
    user: {
      name: string;
      photo: string;
    };
    text: string;
    date: Date;
  }
  
  export interface MediaItem {
    //id: number;      //FMO Eliminacion de columan
    uid_media: string, //FMO Nueva columna
    title: string;
    owner: string;
    type: 'image' | 'video';
    src: string;
    created_at: Date;
    comments: Comment[];
  }
  
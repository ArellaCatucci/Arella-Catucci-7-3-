import { Component , Input} from '@angular/core';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})

export class ContactComponent {
  contacts: {
    facebook?: string;
    instagram?: string;
    email?: string;
    phone?: string;
  } = {};

  ngOnInit() {

    this.contacts.facebook = 'https://www.facebook.com/colegioguevara/';
    this.contacts.email = 'cpdeguevara.sec@tdf.edu.ar';
    this.contacts.instagram = 'colegioguevara';
    this.contacts.phone = '+54 111111111'
    
  }

} 
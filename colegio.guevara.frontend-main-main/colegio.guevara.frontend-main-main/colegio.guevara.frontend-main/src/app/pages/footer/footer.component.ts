import { Component, EventEmitter, Input, Output } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent {

  @Input() titulo:String = '';

  salida:String = '';
  counter:number = 0;

  @Output() enviar = new EventEmitter<number>();

  procesar() {
    this.counter = this.counter + 1;
    this.salida = 'Click';
    this.enviar.emit(this.counter)
    console.log('Click')
  }

  get datos() {
    return this.loginService.datos;
  }


  constructor(private loginService:LoginService) {
    //console.log(this.datos, 'aca')  
  }
}


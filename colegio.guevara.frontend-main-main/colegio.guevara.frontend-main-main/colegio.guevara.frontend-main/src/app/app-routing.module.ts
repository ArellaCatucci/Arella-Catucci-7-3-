import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { ContactComponent} from './contact/contact.component';
import { LoginComponent} from './login/login.component';
import { LogoutComponent } from './logout/logout.component';



const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' }, // Redirigir a 'home' por defecto
  { path: 'home', component: HomeComponent },          // Ruta a HomeComponent
  { path: 'about', component: AboutComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'login', component: LoginComponent },
  { path: 'logout', component: LogoutComponent},
  
  
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { ContactComponent } from './contact/contact.component';
import { LoginComponent } from './login/login.component';
import { HeaderComponent } from './pages/header/header.component';
import { FooterComponent } from './pages/footer/footer.component';

import { LoginService } from './services/login.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LogoutComponent } from './logout/logout.component';
import { MediaCardComponent } from './media/media-card/media-card.component';
import { MediaGalleryComponent } from './media/media-gallery/media-gallery.component';
import { VersionComponent } from './version/version.component';
import { BodyComponent } from './pages/body/body.component';
import { TitleComponent } from './pages/title/title.component';
@NgModule({
  declarations: [
    AppComponent,
    AboutComponent,
    HomeComponent,
    ContactComponent,
    LoginComponent,
    HeaderComponent,
    FooterComponent,
    LogoutComponent,
    MediaCardComponent,
    MediaGalleryComponent,
    VersionComponent,
    BodyComponent,
    TitleComponent,
  
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, 
    HttpClientModule,
    FormsModule
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule { }

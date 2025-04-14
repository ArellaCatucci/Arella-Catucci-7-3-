Instalar ng (herramientas de angular)

sudo apt install npm
sudo apt install ng-common
npm install
npm start


# Revisar
"@angular-devkit/build-angular": "^16.2.0", en en dependencias de dev en package.json

ALTER TABLE tvworld.media_files MODIFY COLUMN `size` float DEFAULT 0 NOT NULL;


# Frontend Coleguio Guevara

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.2.16.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.

* Version Angular 16
nvm use 18

npm install -g @angular/cli@16
npm install bootstrap jquery @popperjs/core

ng serve --host 0.0.0.0 → Permite acceso remoto.

ng g c home
ng g c about
ng g c contact
ng g c login

ng generate service services/auth
ng generate service services/user

ng generate component media/media-card
ng generate component media/media-gallery

* Generacion de documentación


npm install compodoc
npx compodoc -p tsconfig.app.json

/* To learn more about this file see: https://angular.io/config/tsconfig. */
{
"extends": "./tsconfig.json",
"compilerOptions": {
"outDir": "./out-tsc/app",
"types": []
},
"files": [
"src/main.ts"
],
"include": [
"src/**/*.d.ts"
]
}
Quitar .d en include y luego ejecutar npx compodoc -p tsconfig.app.json


IMPORTANTE
sudo chown -R www-data:www-data uploads/

curl -X POST -F "file=@/home/felipe/Vídeos/video.mp4" http://localhost/frontend/public/api/UploadFile


curl 'http://localhost/frontend/public/api/media_files' 

sudo codium --user-data-dir=/home/felipe/.vscodium-root



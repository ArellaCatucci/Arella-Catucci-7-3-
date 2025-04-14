from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator




class UsuarioManager(BaseUserManager):
    """ Manager personalizado para el modelo Usuario """
    def create_user(self, username, password=None, **extra_fields):
        print('Pase!')
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)  # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuario debe tener is_superuser=True")

        return self.create_user(username, password, **extra_fields)

### 📌 Modelo de Usuario con Roles
class Usuario(AbstractUser):
    ROLES = [
        ('alumno', 'Alumno'),
        ('padre', 'Padre'),
        ('profesor', 'Profesor'),
        ('preceptor', 'Preceptor'),
        ('administracion', 'Administración')
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='alumno')
    url = models.CharField(max_length=1024, blank=True, null=True)

    objects = UsuarioManager()  # Asociamos el nuevo manager

    def __str__(self):
        return f"{self.username} - {self.rol}"


### 📌 Modelo de Materia
class Materia(models.Model):
    nombre = models.CharField(max_length=255)
    anio = models.IntegerField(default=0)  # Año de cursada
    contenidos_minimos = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return f"({self.anio})  {self.nombre}" 


### 📌 Modelo de Nota (Cada alumno tiene notas por materia y año)
class Nota(models.Model):
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'alumno'},related_name="notas_alumno")
    profesor_titular = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'}, null=True, blank=True, related_name="notas_profesor" )

    anio = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(7)])
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    cuatrimestre_1_informe_1 = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])  
    cuatrimestre_1_informe_2 = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    cuatrimestre_1_nota = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])

    cuatrimestre_2_informe_1 = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])  
    cuatrimestre_2_informe_2 = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    cuatrimestre_2_nota = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    nota_final = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    

    notas = models.JSONField(blank=True, null=True)  # Guarda las notas como lista JSON

    def __str__(self):
        return f"{self.alumno.username} - {self.materia.nombre}"


### Modelo de Cursada
class Cursada(models.Model):
    alumno = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'alumno'}, related_name="cursada_alumno" )
    preceptor_titular = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'preceptor'}, null=True, blank=True, related_name="cursada_preceptor_titular" )

    anio_calendario = models.IntegerField(validators=[MinValueValidator(2025)], default=2025) 
    anio = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(7)])
    curso = models.CharField(max_length=100)
    asistencia = models.IntegerField(default=0)  
    faltas_injustificadas = models.IntegerField(default=0)  
    faltas_justificadas = models.IntegerField(default=0)  
    

    def __str__(self):
        return f"{self.alumno.username} - {self.curso} - {self.anio}"


from django.db import models

class BoletinImpresion(models.Model):
    alumno = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)
    año = models.IntegerField()

    # Materias con nombres genéricos
    materia_1 = models.CharField(max_length=5, blank=True, null=True)
    materia_2 = models.CharField(max_length=5, blank=True, null=True)
    materia_3 = models.CharField(max_length=5, blank=True, null=True)
    materia_4 = models.CharField(max_length=5, blank=True, null=True)
    materia_5 = models.CharField(max_length=5, blank=True, null=True)
    materia_6 = models.CharField(max_length=5, blank=True, null=True)
    materia_7 = models.CharField(max_length=5, blank=True, null=True)
    materia_8 = models.CharField(max_length=5, blank=True, null=True)
    materia_9 = models.CharField(max_length=5, blank=True, null=True)
    materia_10 = models.CharField(max_length=5, blank=True, null=True)
    materia_11 = models.CharField(max_length=5, blank=True, null=True)
    materia_12 = models.CharField(max_length=5, blank=True, null=True)
    materia_13 = models.CharField(max_length=5, blank=True, null=True)
    materia_14 = models.CharField(max_length=5, blank=True, null=True)

    # Inasistencias
    inasistencias_injustificadas = models.IntegerField(default=0)
    inasistencias_justificadas = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.alumno} - {self.curso} ({self.año})"

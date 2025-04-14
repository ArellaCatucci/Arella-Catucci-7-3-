import os
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2image import convert_from_path
from PIL import Image


from .models import Usuario, Materia, Nota, Cursada, BoletinImpresion

class UsuarioChangeForm(forms.ModelForm):
    """Formulario para editar usuarios en Django Admin, ocultando la contraseña"""
    password = ReadOnlyPasswordHashField(
        help_text="Las contraseñas no se pueden ver aquí. Puedes cambiarlas usando <a href='../password/'>este formulario</a>."
    )

    class Meta:
        model = Usuario
        fields = ('username', 'password', 'rol', 'is_active', 'is_staff')

    def clean_password(self):
        """Evita que la contraseña se reescriba en texto plano"""
        return self.initial["password"]

class UsuarioAdmin(UserAdmin):
    """Configuración de Django Admin para el modelo Usuario"""
    form = UsuarioChangeForm
    list_display = ('username', 'rol', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('rol', 'url')}),
        ('Permisos', {'fields': ('groups', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'rol', 'url', 'is_active', 'is_staff')}
        ),
    )


def exportar_notas_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="notas.pdf"'

    pdf = canvas.Canvas(response)
    pdf.drawString(100, 800, "Listado de Notas")

    y = 780
    for notas in queryset:
        pdf.drawString(100, y, f"{notas.anio} - ${notas.cuatrimestre_1_informe_1}")
        y -= 20

    pdf.showPage()
    pdf.save()
    return response

exportar_notas_pdf.short_description = "Exportar a PDF"

admin.site.register(Permission)



class NotaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'anio' )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Si es superusuario, muestra todo
        return qs.filter(alumno=request.user)  # Filtra por usuario actual


#admin.site.register(Nota) Reemplazado por la registracion de abajo
@admin.register(Nota)
class NotaAdmin(NotaAdmin):
    actions = [exportar_notas_pdf]
    exclude = ('notas',)  # Oculta el campo "anio" en la interfaz de administración
    list_per_page = 20    # Cambia de 100 a 20 registros por página
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Si ya se ingresó un alumno antes, usa ese alumno como predeterminado
        last_nota = Nota.objects.order_by('-id').first()  # Obtiene la última nota ingresada
        # AREARE
        # if last_nota:
        #    form.base_fields['alumno'].initial = last_nota.alumno
        
        return form





#admin.site.register(Materia)
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_per_page = 20    # Cambia de 100 a 20 registros por página



# Registraciones por default
admin.site.register(Usuario, UsuarioAdmin)

#admin.site.register(Boletin)
def generar_boletin_pdf2(modeladmin, request, queryset):
    for boletin in queryset:
        # Configurar respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{boletin.alumno}_boletin.pdf"'

        # Crear PDF
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Encabezado del boletín
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 50, "COLEGIO PROVINCIAL DR. ERNESTO GUEVARA")
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 70, f"Alumno: {boletin.alumno}")
        p.drawString(50, height - 90, f"Curso: {boletin.curso}")
        p.drawString(400, height - 90, f"Año: {boletin.año}")

        # Materias genéricas y sus notas
        y_position = height - 130
        p.setFont("Helvetica-Bold", 10)
        materias = [
            ("Materia 1", boletin.materia_1),
            ("Materia 2", boletin.materia_2),
            ("Materia 3", boletin.materia_3),
            ("Materia 4", boletin.materia_4),
            ("Materia 5", boletin.materia_5),
            ("Materia 6", boletin.materia_6),
            ("Materia 7", boletin.materia_7),
            ("Materia 8", boletin.materia_8),
            ("Materia 9", boletin.materia_9),
            ("Materia 10", boletin.materia_10),
            ("Materia 11", boletin.materia_11),
            ("Materia 12", boletin.materia_12),
            ("Materia 13", boletin.materia_13),
            ("Materia 14", boletin.materia_14),
        ]

        # Dibujar la tabla con las materias y notas
        p.setFont("Helvetica", 10)
        for materia, nota in materias:
            p.drawString(50, y_position, materia)
            p.drawString(400, y_position, nota if nota else "SC")  # SC (Sin Calificación) si está vacío
            y_position -= 20

        # Sección de inasistencias
        y_position -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, "Asistencia:")
        y_position -= 20
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"Inasistencias injustificadas: {boletin.inasistencias_injustificadas}")
        p.drawString(300, y_position, f"Inasistencias justificadas: {boletin.inasistencias_justificadas}")

        # Finalizar el PDF
        p.showPage()
        p.save()
        return response

generar_boletin_pdf2.short_description = "Generar boletín en PDF"



def generar_boletin_pdf(modeladmin, request, queryset):
    for boletin in queryset:
        # Configuración del archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{boletin.alumno}_boletin.pdf"'
        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Dibujar el encabezado
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(width / 2, height - 50, "COLEGIO PROVINCIAL DR. ERNESTO GUEVARA")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 80, f"Apellido y Nombre: {boletin.alumno}")
        pdf.drawString(350, height - 80, f"Curso: {boletin.curso}")
        pdf.drawString(500, height - 80, f"Año: {boletin.año}")

        # Dibujar bordes y estructura de la tabla
        x_start = 50
        y_start = height - 120
        cell_width = 80
        cell_height = 25

        materias = [
            "Matemáticas", "Economía", "Prácticas del Lenguaje", "Geografía",
            "Inglés", "Física", "Salud y Derecho", "Estadística",
            "Diseño Multimedia", "TÉCNICA: Hardware", "TÉCNICA: Programación",
            "TÉCNICA: Redes", "TÉCNICA: Software", "EDI: Arduino"
        ]

        notas = [
            boletin.materia_1, boletin.materia_2, boletin.materia_3, boletin.materia_4,
            boletin.materia_5, boletin.materia_6, boletin.materia_7, boletin.materia_8,
            boletin.materia_9, boletin.materia_10, boletin.materia_11, boletin.materia_12,
            boletin.materia_13, boletin.materia_14
        ]

        # Dibujar encabezados de la tabla
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(x_start, y_start, "Materia")
        pdf.drawString(x_start + 300, y_start, "Nota")

        # Dibujar filas de la tabla
        pdf.setFont("Helvetica", 10)
        y_position = y_start - cell_height

        for i in range(len(materias)):
            pdf.drawString(x_start, y_position, materias[i])
            pdf.drawString(x_start + 300, y_position, notas[i] if notas[i] else "SC")
            pdf.rect(x_start - 5, y_position - 5, 500, cell_height, stroke=1, fill=0)  # Dibujar borde de celda
            y_position -= cell_height

        # Sección de asistencia
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Asistencia:")
        y_position -= 20
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y_position, f"Inasistencias injustificadas: {boletin.inasistencias_injustificadas}")
        pdf.drawString(300, y_position, f"Inasistencias justificadas: {boletin.inasistencias_justificadas}")

        # Dibujar líneas de la tabla de asistencia
        pdf.rect(45, y_position - 5, 500, 25, stroke=1, fill=0)

        # Finalizar el PDF
        pdf.showPage()
        pdf.save()
        return response

generar_boletin_pdf.short_description = "Generar boletín en PDF"


def generar_boletin_jpg(modeladmin, request, queryset):
    for boletin in queryset:
        # Nombre del archivo temporal PDF
        pdf_filename = f"/tmp/{boletin.alumno}_boletin.pdf"
        jpg_filename = f"/tmp/{boletin.alumno}_boletin.jpg"

        # Crear el PDF
        p = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        # Encabezado
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 50, "COLEGIO PROVINCIAL DR. ERNESTO GUEVARA")
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 70, f"Alumno: {boletin.alumno}")
        p.drawString(50, height - 90, f"Curso: {boletin.curso}")
        p.drawString(400, height - 90, f"Año: {boletin.año}")

        # Materias y notas
        y_position = height - 130
        materias = [
            ("Materia 1", boletin.materia_1),
            ("Materia 2", boletin.materia_2),
            ("Materia 3", boletin.materia_3),
            ("Materia 4", boletin.materia_4),
            ("Materia 5", boletin.materia_5),
            ("Materia 6", boletin.materia_6),
            ("Materia 7", boletin.materia_7),
            ("Materia 8", boletin.materia_8),
            ("Materia 9", boletin.materia_9),
            ("Materia 10", boletin.materia_10),
            ("Materia 11", boletin.materia_11),
            ("Materia 12", boletin.materia_12),
            ("Materia 13", boletin.materia_13),
            ("Materia 14", boletin.materia_14),
        ]

        p.setFont("Helvetica", 10)
        for materia, nota in materias:
            p.drawString(50, y_position, materia)
            p.drawString(400, y_position, nota if nota else "SC")
            y_position -= 20

        # Asistencias
        y_position -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, "Asistencia:")
        y_position -= 20
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"Inasistencias injustificadas: {boletin.inasistencias_injustificadas}")
        p.drawString(300, y_position, f"Inasistencias justificadas: {boletin.inasistencias_justificadas}")

        # Guardar PDF
        p.showPage()
        p.save()

        # Convertir PDF a Imagen JPG
        images = convert_from_path(pdf_filename)
        images[0].save(jpg_filename, "JPEG")

        # Leer el archivo JPG para la respuesta
        with open(jpg_filename, "rb") as image_file:
            response = HttpResponse(image_file.read(), content_type="image/jpeg")
            response['Content-Disposition'] = f'attachment; filename="{boletin.alumno}_boletin.jpg"'

        # Limpiar archivos temporales
        os.remove(pdf_filename)
        os.remove(jpg_filename)

        return response



@admin.register(BoletinImpresion)
class BoletinImpresionAdmin(admin.ModelAdmin):
    list_display = ("alumno", "curso", "año")
    actions = [generar_boletin_pdf, generar_boletin_jpg]

admin.site.register(Cursada)

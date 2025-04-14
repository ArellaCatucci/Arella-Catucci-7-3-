from rest_framework import serializers
from .models import Usuario, Materia, Nota, Cursada

### 📌 Serializador para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']

### 📌 Serializador para Materia
class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

### 📌 Serializador para Nota
class NotaSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()  # Anida la información de la materia
    alumno = serializers.StringRelatedField()  # Muestra el nombre del alumno

    class Meta:
        model = Nota
        fields = ['id', 'alumno', 'materia', 'anio', 'notas']

### 📌 Serializador para Cursada
class CursadaSerializer(serializers.ModelSerializer):
    alumno = UsuarioSerializer()  # Incluye datos del alumno
    notas = serializers.SerializerMethodField()  # Extrae las notas del alumno

    class Meta:
        model = Cursada
        fields = ['id', 'colegio', 'alumno', 'curso', 'periodos', 'inasistencia', 'notas']

    def get_notas(self, obj):
        """
        Obtiene todas las notas del alumno relacionadas con el boletín.
        """
        notas = Nota.objects.filter(alumno=obj.alumno, anio=obj.periodos[-1])
        return NotaSerializer(notas, many=True).data

from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Usuario, Materia, Nota, Cursada
from .serializers import UsuarioSerializer, MateriaSerializer, NotaSerializer, CursadaSerializer
from django.core.cache import cache
from django.views.decorators.cache import cache_page

### 📌 Vista para obtener el usuario autenticado
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

### 📌 Vista para obtener todas las materias
class MateriaListView(APIView):
    permission_classes = [AllowAny]  # Permite que cualquiera consulte las materias

    def get(self, request):
        materias = Materia.objects.all()
        serializer = MateriaSerializer(materias, many=True)
        return Response(serializer.data)

### 📌 Vista para obtener todas las notas de un alumno en un año específico
class NotasPorAlumnoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, alumno_id, anio):
        alumno = get_object_or_404(Usuario, id=alumno_id, rol="alumno")
        notas = Nota.objects.filter(alumno=alumno, anio=anio)
        serializer = NotaSerializer(notas, many=True)
        return Response(serializer.data)

### 📌 Vista para obtener el boletín de un alumno
class CursadaPorAlumnoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, alumno_id):
        cursada = get_object_or_404(Boletin, alumno_id=alumno_id)
        serializer = CursadaSerializer(cursada)
        return Response(serializer.data)

### 📌 Vista para registrar una nueva nota
class CrearNotaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
from .utils import obtener_datos, generar_grafico_evolucion

@cache_page(3600)  # Caché de 1 hora
def generar_grafico_view(request, alumno_id):
    # Intenta obtener el gráfico desde la caché
    cache_key = f"grafico_{alumno_id}"
    grafico_path = cache.get(cache_key)

    if not grafico_path:
        df = obtener_datos(alumno_id=alumno_id, anio_calendario=2025)
        if df.empty:
            return HttpResponse("No hay datos disponibles para este alumno.", status=404)

        grafico_path = generar_grafico_evolucion(df)
        cache.set(cache_key, grafico_path, timeout=3600)  # Guarda en caché por 1 hora

    return FileResponse(open(grafico_path, 'rb'), content_type="image/png")   
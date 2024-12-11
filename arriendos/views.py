from rest_framework import viewsets
from .models import Habitacion, Reserva, Pago
from .serializers import HabitacionSerializer, ReservaSerializer, PagoSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from .forms import ReservaForm  # Suponiendo que tienes un formulario para la reserva
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Habitacion
from .forms import HabitacionForm


class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

# Vista para mostrar el formulario de reserva
def reserva_formulario(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    
    if request.method == 'POST':
        # Usamos el formulario de Django para procesar los datos
        form = ReservaForm(request.POST)
        
        if form.is_valid():
            # Creamos la reserva, pero primero verificamos la disponibilidad
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion

            if not reserva.disponibilidad():
                # Si la habitación no está disponible, mostramos un mensaje de error
                form.add_error(None, "La habitación no está disponible en esas fechas.")
            else:
                reserva.save()  # Guardamos la reserva
                return HttpResponse("Reserva realizada con éxito")

    else:
        form = ReservaForm()

    return render(request, 'formulario_reserva.html', {
        'habitacion': habitacion,
        'form': form
    })

# Vista para mostrar la lista de habitaciones disponibles
def listado_habitaciones(request):
    habitaciones = Habitacion.objects.filter(disponible=True)  # Filtramos solo las habitaciones disponibles
    return render(request, 'listado_habitaciones.html', {
        'habitaciones': habitaciones
    })

# Vista principal de la aplicación
def home(request):
    return render(request, 'home.html')

# Vista para crear una reserva mediante la API
@api_view(['POST'])
def crear_reserva(request):
    if request.method == 'POST':
        habitacion_numero = request.data.get('habitacion')  # Ahora se recibe un número
        habitacion = Habitacion.objects.get(numero=habitacion_numero)  # Buscar por número de habitación
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')
        usuario = request.data.get('usuario')
        total_pago = request.data.get('total_pago')
        estado = request.data.get('estado')

        reserva = Reserva.objects.create(
            habitacion=habitacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            usuario=usuario,
            total_pago=total_pago,
            estado=estado
        )

        # Serializar la reserva para devolverla como respuesta
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def listado_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'html/listado_habitaciones.html', {'habitaciones': habitaciones})


def agregar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_habitaciones')  # Redirige a la lista de habitaciones
    else:
        form = HabitacionForm()

    return render(request, 'html/agregar_habitacion.html', {'form': form})
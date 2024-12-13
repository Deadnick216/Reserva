from rest_framework import viewsets
from .models import Habitacion, Reserva, Pago
from .serializers import HabitacionSerializer, ReservaSerializer, PagoSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from .forms import ReservaForm
from django.shortcuts import redirect
from .models import Habitacion
from .forms import HabitacionForm
from django.shortcuts import render
from .models import Reserva  
from django.test import TestCase
from django.urls import reverse


class ReservaViewTests(TestCase):
    def test_detalle_reserva(self):
        response = self.client.get(reverse('detalle_reserva', kwargs={'habitacion_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reserva')

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

    return render(request, 'detalle_reserva.html', {
        'habitacion': habitacion,
        'form': form
    })

# Vista para mostrar la lista de habitaciones disponibles
def listado_habitaciones(request):
    habitaciones = Habitacion.objects.filter(estado='Disponible')  # Filtramos por habitaciones disponibles
    return render(request, 'listado_habitaciones.html', {'habitaciones': habitaciones})

# Vista principal de la aplicación
def home(request):
    return render(request, 'home.html')

@api_view(['POST'])
def crear_reserva(request):
    if request.method == 'POST':
        # Recibe los datos del formulario
        habitacion_id = request.POST.get('habitacion_id')  # Este ID debe venir desde el formulario
        habitacion = Habitacion.objects.get(id=habitacion_id)
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        usuario = request.POST.get('usuario')
        total_pago = request.POST.get('total_pago')
        estado = request.POST.get('estado')

        # Crear la reserva
        reserva = Reserva.objects.create(
            habitacion=habitacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            usuario=usuario,
            total_pago=total_pago,
            estado=estado
        )

        # Cambiar el estado de la habitación a 'Reservada'
        habitacion.estado = 'Reservada'
        habitacion.save()

        # Mostrar un mensaje de éxito
        return HttpResponse("Reserva realizada con éxito.")

def agregar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_habitaciones')  # Redirige a la lista de habitaciones
    else:
        form = HabitacionForm()

    return render(request, 'html/agregar_habitacion.html', {'form': form})

# Vista para reservar una habitación
def reservar_habitacion(request):
    if request.method == "POST":
        habitacion_id = request.POST.get("habitacion_id")  # Obtenemos el ID de la habitación
        habitacion = Habitacion.objects.get(id=habitacion_id)  # Obtenemos la habitación por ID
        habitacion.estado = "Reservada"  # Cambiamos el estado a "Reservada"
        habitacion.save()  # Guardamos los cambios
        return redirect('listado_habitaciones')  # Redirigimos a la vista de listado de habitaciones

    habitaciones = Habitacion.objects.all()  # Traemos todas las habitaciones
    return render(request, 'html/reservar_habitacion.html', {'habitaciones': habitaciones})

def registrar_habitacion(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        capacidad = request.POST['capacidad']
        estado = request.POST.get('estado', 'Disponible')

        # Crear la nueva habitación
        Habitacion.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            capacidad=capacidad,
            estado=estado,
        )

        # Redirigir al listado de habitaciones después de registrar
        return redirect('listado_habitaciones')  # Redirige a la ruta de listado de habitaciones

    return render(request, 'registrar_habitacion.html')

def detalle_reserva(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion
            reserva.save()
            
            # Cambiar el estado de la habitación a "Reservada"
            habitacion.estado = 'Reservada'
            habitacion.save()

            # Mensaje de éxito
            messages.success(request, "¡Reserva realizada con éxito!")

            # Redirigir a la página de inicio
            return redirect('home')  # Redirige a la página principal donde se muestra el mensaje

    else:
        form = ReservaForm()

    return render(request, 'detalle_reserva.html', {'habitacion': habitacion, 'form': form})

def confirmacion_reserva(request, reserva_id):
    try:
        # Buscar la reserva por su ID
        reserva = Reserva.objects.get(id=reserva_id)
        # Renderizar la plantilla con los detalles de la reserva
        return render(request, 'confirmacion_reserva.html', {'reserva': reserva})
    except Reserva.DoesNotExist:
        # Si no se encuentra la reserva, devolver un error 404
        return render(request, '404.html', {'message': 'Reserva no encontrada'}, status=404)

def confirmacion_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'confirmacion_reserva.html', {'reserva': reserva})

def guardar_reserva(request):
    if request.method == 'POST':
        habitacion_id = request.POST.get('habitacion_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        usuario = request.POST.get('usuario')
        # Obtener la habitación
        habitacion = get_object_or_404(Habitacion, id=habitacion_id)

        # Guardar la reserva
        reserva = Reserva(
            habitacion=habitacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            usuario=usuario,
        )
        reserva.save()

        # Cambiar el estado de la habitación
        habitacion.estado = 'Reservada'
        habitacion.save()

        return HttpResponse({'message': 'Reserva realizada con éxito'})

    return HttpResponse({'error': 'Método no permitido'}, status=405)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitacionViewSet, ReservaViewSet, PagoViewSet
from . import views 

# Router para las vistas de API
router = DefaultRouter()
router.register(r'habitaciones', HabitacionViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # API de habitaciones, reservas y pagos
    path('api/', include(router.urls)),

    # Listado de habitaciones
    path('habitaciones/', views.listado_habitaciones, name='listado_habitaciones'),

    # Detalle y reserva de una habitación
    path('habitaciones/reservar/<int:habitacion_id>/', views.reservar_habitacion, name='reservar_habitacion'),

    # Formulario para reserva de habitación
    path('habitacion/<int:habitacion_id>/reserva/', views.reserva_formulario, name='reserva_formulario'),

    # Otras funcionalidades relacionadas con habitaciones y reservas
    path('habitaciones/agregar/', views.agregar_habitacion, name='agregar_habitacion'),
    path('habitaciones/registrar/', views.registrar_habitacion, name='registrar_habitacion'),

    # API específica para crear reservas
    path('crear_reserva/', views.crear_reserva, name='crear_reserva_api'),

    # Detalle de reserva
    path('habitaciones/detalle/<int:habitacion_id>/', views.detalle_reserva, name='detalle_reserva'),

    # Confirmación de reserva
    path('reservas/confirmacion/<int:reserva_id>/', views.confirmacion_reserva, name='confirmacion_reserva'),

    path('guardar_reserva/', views.guardar_reserva, name='guardar_reserva'),
]

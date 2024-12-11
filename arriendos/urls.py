from django.urls import path, include
from .views import home
from rest_framework.routers import DefaultRouter
from .views import HabitacionViewSet, ReservaViewSet, PagoViewSet
from . import views 

router = DefaultRouter()
router.register(r'habitaciones', HabitacionViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la raíz
    path('api/', include(router.urls)),  # API de habitaciones, reservas y pagos
    path('habitaciones/', views.listado_habitaciones, name='listado_habitaciones'),
    path('habitacion/<int:habitacion_id>/reserva/', views.reserva_formulario, name='reserva_formulario'),
    path('habitaciones/agregar/', views.agregar_habitacion, name='agregar_habitacion'),

]

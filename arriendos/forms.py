# arriendos/forms.py
from django import forms
from .models import Reserva
from .models import Habitacion  # Asegúrate de que tienes un modelo llamado Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'fecha_fin', 'habitacion', 'usuario', 'total_pago', 'estado'] 


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['nombre', 'descripcion', 'precio', 'capacidad', 'estado', 'direccion']
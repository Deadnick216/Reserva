from django.db import models

class Habitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('Reservada', 'Reservada')], default='Disponible')
    direccion = models.CharField(max_length=255)  # Campo para la dirección de la habitación

    def __str__(self):
        return f'{self.nombre} - {self.estado}'
        
class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.CharField(max_length=255)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Hacerlo opcional
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], null=True, blank=True)  # Hacerlo opcional
    
    def disponibilidad(self):
        # Verificar si hay reservas existentes en las fechas solicitadas
        reservas_existentes = Reserva.objects.filter(
            habitacion=self.habitacion,
            fecha_inicio__lt=self.fecha_fin,
            fecha_fin__gt=self.fecha_inicio
        )
        return not reservas_existentes.exists()
    
    def save(self, *args, **kwargs):
        if not self.disponibilidad():
            raise ValueError("La habitación no está disponible en esas fechas.")
        super().save(*args, **kwargs)

class Pago(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago de {self.monto} para la reserva {self.reserva.id}"

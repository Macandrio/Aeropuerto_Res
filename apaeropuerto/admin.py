from django.contrib import admin
from .models import (
    Aeropuerto, Vuelo, Pasajero, Equipaje, Aerolinea,
    VueloAerolinea, Reserva, Empleado, Asiento, Servicio , ContactoAeropuerto , EstadisticasVuelo ,
)


# Registrar todos los modelos de manera básica
admin.site.register(Aeropuerto)
admin.site.register(Vuelo)
admin.site.register(Pasajero)
admin.site.register(Equipaje)
admin.site.register(Aerolinea)
admin.site.register(VueloAerolinea)
admin.site.register(Reserva)
admin.site.register(Empleado)
admin.site.register(Asiento)
admin.site.register(Servicio)
admin.site.register(ContactoAeropuerto)
admin.site.register(EstadisticasVuelo)
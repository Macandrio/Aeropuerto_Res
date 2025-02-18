from django.urls import path

from  .api_views import *



urlpatterns = [
    path('Aeropuerto',lista_aeropuerto, name='lista_aeropuerto'),
    path('Aerolinea',lista_aerolinea, name='lista_aerolinea'),
    path('Vuelo',lista_vuelo, name='lista_vuelo'),
    path('Reserva',lista_reserva, name='lista_reserva'),
    path('Vueloaerolinea',lista_vueloaerolinea, name='lista_vueloaerolinea'),



    # Formularios

    #Obtener
    path('Aeropuerto/', Aeropuertos_obtener),
    path('Aeropuerto/<int:aeropuerto_id>', Aeropuerto_obtener),  
    path('Aerolinea/<int:aerolinea_id>', Aerolinea_obtener),
    path('Aerolineas/', Aerolinea_obtener),
    path('Pasajeros/', Pasajeros_obtener),
    path('Usuario/<int:usuario_id>', Usuario_obtener),
    path('Vuelos/', Vuelo_obtener),
    path('Reserva/<int:reserva_id>', Reserva_obtener_id),
    path('Reservas/', Reserva_obtener),

    # Buscar
    path('Aeropuerto/busqueda_simple', Aeropuerto_buscar),
    path('Aeropuerto/busqueda_avanzada', Aeropuerto_buscar_avanzado),
    path('Aerolinea/busqueda_avanzada', Aerolinea_buscar_avanzado), 
    path('Estadisticas/busqueda_avanzada', Estadisticas_buscar_avanzado),  
    path('Reservas/busqueda_avanzada', Reservas_buscar_avanzado),
    path('VueloAerolinea/busqueda_avanzada', VueloAerolinea_buscar_avanzado),

    # Crear
    path('Aeropuerto/Crear', Aeropuerto_create),
    path('Aerolinea/Crear', Aerolinea_create),
    path('Reserva/Crear', Reserva_create),
    path('VueloAerolinea/Crear', VueloAerolinea_create),


    # Editar
    path('Aeropuerto/editar/<int:aeropuerto_id>', Aeropuerto_editar),
    path('Aerolinea/editar/<int:aerolinea_id>', Aerolinea_editar),
    path('Reserva/editar/<int:reserva_id>', Reserva_editar),

    # Actualizar
    path('Aeropuerto/actualizar/nombre/<int:aeropuerto_id>',Aeropuerto_actualizar_nombre),
    path('Aerolinea/actualizar/nombre/<int:aerolinea_id>',Aerolinea_actualizar_nombre),
    path('Reserva/actualizar/codigo/<int:reserva_id>',Reserva_actualizar_codigo),

    # Eliminar
    path('Aeropuerto/eliminar/<int:aeropuerto_id>',Aeropuerto_eliminar),
    path('Aerolinea/eliminar/<int:aerolinea_id>',Aerolinea_eliminar),
    path('Reserva/eliminar/<int:reserva_id>',Reserva_eliminar),
    
]
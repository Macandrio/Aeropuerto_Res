from django.urls import path

from  .api_views import *



urlpatterns = [
    path('Aeropuerto',lista_aeropuerto, name='lista_aeropuerto'),
    path('Aerolinea',lista_aerolinea, name='lista_aerolinea'),
    path('Vuelo',lista_vuelo, name='lista_vuelo'),
    path('Reserva',lista_reserva, name='lista_reserva'),
    path('Vueloaerolinea',lista_vueloaerolinea, name='lista_vueloaerolinea'),



    #Formularios 

    # Buscar
    path('Aeropuerto/<int:aeropuerto_id>', Aeropuerto_obtener),
    path('Aeropuerto/busqueda_simple', Aeropuerto_buscar),
    path('Aeropuerto/busqueda_avanzada', Aeropuerto_buscar_avanzado),
    path('Aerolinea/busqueda_avanzada', Aerolinea_buscar_avanzado), 
    path('Estadisticas/busqueda_avanzada', Estadisticas_buscar_avanzado),  
    path('Reservas/busqueda_avanzada', Reservas_buscar_avanzado),

    #Crear
    path('Aeropuerto/Crear', Aeropuerto_create),
]
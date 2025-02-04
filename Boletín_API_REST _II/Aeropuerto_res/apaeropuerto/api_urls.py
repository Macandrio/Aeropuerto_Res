from django.urls import path

from  .api_views import *



urlpatterns = [
    path('Aeropuerto',lista_aeropuerto, name='lista_aeropuerto'),
    path('Aerolinea',lista_aerolinea, name='lista_aerolinea'),
    path('Vuelo',lista_vuelo, name='lista_vuelo'),
    path('Reserva',lista_reserva, name='lista_reserva'),
    path('Vueloaerolinea',lista_vueloaerolinea, name='lista_vueloaerolinea'),



    #Formularios
    path('Aeropuerto/<int:libro_id>', Aeropuerto_obtener),
    path('Aeropuerto/busqueda_simple', Aeropuerto_buscar),

    
]
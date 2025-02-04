from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aeropuerto/', views.lista_aeropuerto, name='lista_aeropuerto'),
    path('vuelo/', views.lista_vuelo, name='lista_vuelo'),
    path('pasajero/', views.lista_pasajero, name='lista_pasajero'),
    path('equipaje/', views.lista_equipaje, name='lista_equipaje'),
    path('aerolineas/', views.lista_aerolineas, name='lista_aerolineas'),
    path('vuelos_aerolineas/', views.lista_vuelos_aerolineas, name='lista_vuelos_aerolineas'),
    path('reserva/', views.lista_reserva, name='lista_reserva'),
    path('empleado/', views.lista_empleado, name='lista_empleado'),
    path('silla/', views.lista_silla, name='lista_silla'),
    path('servicio/', views.lista_servicio, name='lista_servicio'),
    path('contactoaeropuerto/', views.lista_ContactoAeropuerto, name='lista_ContactoAeropuerto'),
    path('estadisticasvuelo/', views.lista_EstadisticasVuelo, name='lista_EstadisticasVuelo'),
    
    #QuerySet
    path('pasajero-vuelo/<int:id_vuelo>/', views.pasajeros_vuelo, name='pasajeros_vuelo'),
    path('vuelo-volando-año/<int:anyo>/', views.vuelo_volando_año, name='vuelo_volando_año'),
    path('texto-vuelo-aerolinea/<int:id_aerolinea>/<str:texto_buscar>/', views.texto_vuelo_aerolinea, name='texto_vuelo_aerolinea'),
    path('historial-feedbacks-pasajero/<int:pasajero_id>/', views.historial_feedbacks_pasajero, name='historial_feedbacks_pasajero'),
    path('vuelos-origen-destino/<int:origen_id>/<int:destino_id>/', views.vuelos_origen_destino, name='vuelos_origen_destino'),
    re_path(r'^reservas/(?P<metodo_pago>\w+)/(?P<año>\d{4})/$', views.reservas_por_metodo_y_año, name='reservas_por_metodo_y_año'),
    path('vuelos/cortos/<int:origen_id>/<int:destino_id>/<int:estado>/', views.vuelos_cortos_origen_destino, name='vuelos_cortos_origen_destino'),
    path('peso-equipaje-vuelo/<int:vuelo_id>/', views.peso_equipaje_vuelo, name='peso_equipaje_vuelo'),
    path('vuelos-sin-operacion/<int:aerolinea_id>/', views.vuelos_sin_operacion, name='vuelos_sin_operacion'),
    path('consulta/pasajeros-vuelo/<int:id_vuelo>/', views.cuantos_pasajeros_vuelo, name='cuantos_pasajeros_vuelo'),

    #Formulario

    #Aeropuerto
    path('aeropuerto/crear/', views.crear_aeropuerto, name='crear_aeropuerto'),
    path('aeropuerto/busqueda/', views.Aeropuerto_buscar_avanzado, name='Aeropuerto_buscar_avanzado'),
    path('aeropuerto/editar/<int:aeropuerto_id>/', views.editar_aeropuerto, name='editar_aeropuerto'),
    path('aeropuerto/eliminar/<int:aeropuerto_id>/', views.eliminar_aeropuerto, name='eliminar_aeropuerto'),

    #contacto aeropuerto
    path('contacto_aeropuerto/crear/', views.crear_contacto, name='crear_contacto'),
    path('contacto_aeropuerto/buscar/', views.contacto_Aeropuerto_buscar_avanzado, name='contacto_Aeropuerto_buscar_avanzado'),
    path('contacto_aeropuerto/modificar/<int:contacto_id>', views.contacto_Aeropuert_modificar, name='contacto_Aeropuert_modificar'),
    path('contacto/eliminar/<int:contacto_id>',views.contacto_Aeropuert_eliminar,name='contacto_Aeropuert_eliminar'),


    #Aerolinea
    path('Aerolinea/crear/', views.crear_Aerolinea, name='crear_Aerolinea'),
    path('Aerolinea/buscar/', views.Aerolinea_buscar_avanzado, name='Aerolinea_buscar_avanzado'),
    path('Aerolinea/modificar/<int:aerolinea_id>', views.Aerolinea_modificar, name='Aerolinea_modificar'),
    path('Aerolinea/eliminar/<int:aerolinea_id>',views.Aerolinea_eliminar,name='Aerolinea_eliminar'),
    
    #Vuelo
    path('Vuelo/crear/', views.crear_Vuelo, name='crear_Vuelo'),
    path('Vuelo/buscar/', views.Vuelo_buscar_avanzado, name='Vuelo_buscar_avanzado'),
    path('Vuelo/modificar/<int:vuelo_id>',views.Vuelo_modificar,name='Vuelo_modificar'),
    path('Vuelo/eliminar/<int:vuelo_id>',views.Vuelo_eliminar,name='Vuelo_eliminar'),

    #Pasajero
    path('Pasajero/crear/', views.crear_pasajero, name='crear_pasajero'),
    path('Pasajero/buscar/', views.Pasajero_buscar_avanzado, name='Pasajero_buscar_avanzado'),
    path('Pasajero/modificar/<int:pasajero_id>',views.Pasajero_modificar,name='Pasajero_modificar'),
    path('Pasajero/eliminar/<int:pasajero_id>',views.Pasajero_eliminar,name='Pasajero_eliminar'),

    #EstadisticasVuelo
    path('estadisticasvuelo/crear/', views.crear_estadisticasvuelo, name='crear_estadisticasvuelo'),
    path('estadisticasvuelo/buscar/', views.Estadisticas_buscar_avanzado, name='Estadisticas_buscar_avanzado'),
    path('estadisticasvuelo/modificar/<int:estadisticas_id>',views.Estadisticas_modificar,name='Estadisticas_modificar'),
    path('estadisticasvuelo/eliminar/<int:estadisticas_id>',views.Estadisticas_eliminar,name='Estadisticas_eliminar'),

    #Reservas
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/buscar/', views.Reserva_buscar_avanzado, name='Reserva_buscar_avanzado'),
    path('reservas/modificar//<int:reserva_id>', views.editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:reserva_id>',views.reserva_eliminar,name='reserva_eliminar'),


    #USUARIO
    path('registrar',views.registrar_usuario,name='registrar_usuario'),



]

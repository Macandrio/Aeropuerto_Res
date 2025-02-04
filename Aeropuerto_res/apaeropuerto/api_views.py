from .models import *
from .serializers import *
from .forms import * 
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

    
@api_view(['GET'])
def lista_aeropuerto(request):

    aeropuerto = Aeropuerto.objects.prefetch_related(
    Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
    Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
    Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
    Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
)
    serializer = AeropuertoSerializer(aeropuerto, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_aerolinea(request):
    
    aerolinea = Aerolinea.objects.prefetch_related(
    Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
    Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
)
    serializer = AerolineaSerializer(aerolinea, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_vuelo(request):
    
    vuelo = Vuelo.objects.prefetch_related(
    Prefetch('vuelo_pasajero'),           # ManyToMany con Pasajero
    Prefetch('asiento_vuelo'),            # ManyToOne con Asiento
    Prefetch('vuelo_media_aerolinea'),    # ManyToOne con VueloAerolinea
    Prefetch('vuelo_datos')               # OneToOne con EstadisticasVuelo
).select_related(
    'origen',                             # ManyToOne con Aeropuerto (origen)
    'destino'                             # ManyToOne con Aeropuerto (destino)
)
    #serializer = LibroSerializer(libros, many=True)
    serializer = VueloSerializer(vuelo, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def lista_reserva(request):
    
    reserva = Reserva.objects.select_related(
    'pasajero',                           # ManyToOne con Pasajero
)
    serializer = ReservaSerializer(reserva, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lista_vueloaerolinea(request):
    
    vuelosaerolinea = VueloAerolinea.objects.select_related(
        'aerolinea',   # ForeignKey directa a Aerolinea
        'vuelo'        # ForeignKey directa a Vuelo
    )

    serializer = VueloAerolineaSerializer(vuelosaerolinea, many=True)
    return Response(serializer.data)


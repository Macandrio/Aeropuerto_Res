from .models import *
from .serializers import *
from .forms import * 
from django.db.models import Q,Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


#----------------------------------------------Listar----------------------------------------------------------------
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

#----------------------------------------------Formularios----------------------------------------------------------------

#Obtener Aeropuertos por id
@api_view(['GET']) 
def Aeropuerto_obtener(request,aeropuerto_id):
    aeropuerto = Aeropuerto.objects.prefetch_related(
    Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
    Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
    Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
    Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
)
    aeropuerto = Aeropuerto.get(id=aeropuerto_id)
    serializer = AeropuertoSerializer(aeropuerto)
    return Response(serializer.data)

#Aeropuerto Buscar
@api_view(['GET'])
def Aeropuerto_buscar(request):
    formulario = BusquedaAeropuertoForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        aeropuerto = Aeropuerto.objects.prefetch_related(
            Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
            Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
            Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
            Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
        )
        aeropuerto = aeropuerto.filter(nombre__contains=texto).all()
        serializer = AeropuertoSerializer(aeropuerto, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Aeropuerto_buscar_avanzado(request):
    if len(request.query_params) > 0:

        formulario = BusquedaAvanzadaAeropuertoForm(request.query_params)

        if formulario.is_valid():
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda','')
            QSaeropuerto = Aeropuerto.objects.prefetch_related(
                Prefetch('aerolinea_de_aeropuerto'),
                Prefetch('vuelos_de_origen'),
                Prefetch('vuelos_de_destino'),
                Prefetch('servicio_aeropuerto')
            )

            # Obtener los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            ciudades = formulario.cleaned_data.get('ciudades')
            paises = formulario.cleaned_data.get('pais')

            # Aplicar filtros dinámicamente
            if textoBusqueda:
                QSaeropuerto = QSaeropuerto.filter(nombre__icontains=textoBusqueda)

            if ciudades:
                filtro_ciudad = Q(ciudad=ciudades[0])
                for ciudad in ciudades[1:]:
                    filtro_ciudad |= Q(ciudades=ciudad)
                    QSaeropuerto = QSaeropuerto.filter(filtro_ciudad)

            if paises:
                filtro_pais = Q(pais=paises[0])
                for pais in paises[1:]:
                    filtro_pais |= Q(pais=pais)
                QSaeropuerto = QSaeropuerto.filter(filtro_pais)

            # Obtener resultados y serializar
            aeropuerto = QSaeropuerto.all()
            serializer = AeropuertoSerializer(aeropuerto, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def Aerolinea_buscar_avanzado(request):
    if len(request.query_params) > 0:

        formulario = BusquedaAvanzadaAerolinea(request.query_params)

        if formulario.is_valid():
            QSaerolinea = Aerolinea.objects.prefetch_related(
                            Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
                            Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
                        )


            # Obtener los filtros del formulario
            nombre = formulario.cleaned_data.get('nombre')
            codigo = formulario.cleaned_data.get('codigo')
            fecha_fundacion = formulario.cleaned_data.get('fecha_fundacion')  # Lista de ciudades
            pais = formulario.cleaned_data.get('pais')  # Lista de países

            # Aplicar filtros dinámicamente
            if nombre:
                QSaerolinea = QSaerolinea.filter(nombre__icontains=nombre)

            if codigo:
                QSaerolinea = QSaerolinea.filter(codigo__icontains=codigo)

            if fecha_fundacion:
                QSaerolinea = QSaerolinea.filter(fecha_fundacion__gte=fecha_fundacion)

            if pais:
                QSaerolinea = QSaerolinea.filter(pais=pais)

            # Obtener resultados y serializar
            aeropuerto = QSaerolinea.all()
            serializer = AerolineaSerializer(aeropuerto, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def Estadisticas_buscar_avanzado(request):
    if len(request.query_params) > 0:

        formulario = BusquedaAvanzadaEstadisticas(request.query_params)

        if formulario.is_valid():
            QSaerolinea = EstadisticasVuelo.objects.select_related('vuelo')


            # Obtener los filtros del formulario
            fecha_estadisticas = formulario.cleaned_data.get('fecha_estadisticas')
            numero_asientos_vendidos = formulario.cleaned_data.get('numero_asientos_vendidos')
            numero_cancelaciones = formulario.cleaned_data.get('numero_cancelaciones')  # Lista de ciudades
            feedback_pasajeros = formulario.cleaned_data.get('feedback_pasajeros')  # Lista de países
            
            # Aplicar filtros dinámicamente
            if fecha_estadisticas:
                QSaerolinea = QSaerolinea.filter(fecha_estadisticas__gte=fecha_estadisticas) #Mayor o igual 

            if numero_asientos_vendidos:
                QSaerolinea = QSaerolinea.filter(numero_asientos_vendidos__lte=numero_asientos_vendidos) 
            
            if numero_cancelaciones:
                QSaerolinea = QSaerolinea.filter(numero_cancelaciones__gte=numero_cancelaciones)#menor o igual

            if feedback_pasajeros:
                QSaerolinea = QSaerolinea.filter(feedback_pasajeros__icontains=feedback_pasajeros)


            # Obtener resultados y serializar
            esadisticas = QSaerolinea.all()
            serializer = EstadisticasSerializer(esadisticas, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
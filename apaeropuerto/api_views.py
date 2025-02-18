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
    'pasajero',
    'vuelo'
)
    serializer = ReservaSerializer(reserva, many=True)
    return Response(serializer.data)

#--------------------------------------Formularios_Buscar----------------------------------------------------------------

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
                filtro_ciudad = Q(ciudades=ciudades[0])
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
            QSestadisticas = EstadisticasVuelo.objects.select_related('vuelo')


            # Obtener los filtros del formulario
            fecha_estadisticas = formulario.cleaned_data.get('fecha_estadisticas')
            numero_asientos_vendidos = formulario.cleaned_data.get('numero_asientos_vendidos')
            numero_cancelaciones = formulario.cleaned_data.get('numero_cancelaciones')  # Lista de ciudades
            feedback_pasajeros = formulario.cleaned_data.get('feedback_pasajeros')  # Lista de países
            
            # Aplicar filtros dinámicamente
            if fecha_estadisticas:
                QSestadisticas = QSestadisticas.filter(fecha_estadisticas__gte=fecha_estadisticas) #Mayor o igual 

            if numero_asientos_vendidos:
                QSestadisticas = QSestadisticas.filter(numero_asientos_vendidos__lte=numero_asientos_vendidos) 
            
            if numero_cancelaciones:
                QSestadisticas = QSestadisticas.filter(numero_cancelaciones__gte=numero_cancelaciones)#menor o igual

            if feedback_pasajeros:
                QSestadisticas = QSestadisticas.filter(feedback_pasajeros__icontains=feedback_pasajeros)


            # Obtener resultados y serializar
            esadisticas = QSestadisticas.all()
            serializer = EstadisticasSerializer(esadisticas, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def Reservas_buscar_avanzado(request):
    if len(request.query_params) > 0:

        formulario = BusquedaAvanzadaReservaForm(request.query_params)

        if formulario.is_valid():
            QSreserva = Reserva.objects.select_related(
                                'pasajero',
                                'vuelo'                             
                            )

            # Obtener los filtros del formulario
            metodo_pago = formulario.cleaned_data.get('metodo_pago')
            fecha_reserva = formulario.cleaned_data.get('fecha_reserva')
            estado_de_pago = formulario.cleaned_data.get('estado_de_pago')

            # Aplicar filtros dinámicamente
            if metodo_pago:
                QSreserva = QSreserva.filter(metodo_pago=metodo_pago)

            if fecha_reserva:
                QSreserva = QSreserva.filter(fecha_reserva__gte=fecha_reserva) #Mayor o igual 

            if estado_de_pago is not None:
                QSreserva = QSreserva.filter(estado_de_pago=estado_de_pago) 

            # Obtener resultados y serializar
            reserva = QSreserva.all()
            serializer = ReservaSerializer(reserva, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

#--------------------------------------Formularios_Obtener----------------------------------------------------------------

#Obtener Aeropuertos por id
@api_view(['GET']) 
def Aeropuerto_obtener(request,aeropuerto_id):
    aeropuerto = Aeropuerto.objects.prefetch_related(
    Prefetch('contacto_de_aeropuerto'),
    Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
    Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
    Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
    Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
).get(id=aeropuerto_id)
    serializer = AeropuertoSerializer(aeropuerto)
    return Response(serializer.data)


#Obtener Aeropuertos
@api_view(['GET']) 
def Aeropuertos_obtener(request):
    aeropuerto = Aeropuerto.objects.prefetch_related(
    Prefetch('contacto_de_aeropuerto'),
    Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
    Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
    Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
    Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
)
    serializer = AeropuertoSerializer(aeropuerto, many=True)  # ✅ Se añade many=True para manejar una lista
    return Response(serializer.data)


#Obtener Aerolinea por id
@api_view(['GET']) 
def Aerolinea_obtener_id(request,aerolinea_id):
    aerolinea = Aerolinea.objects.prefetch_related(
                    Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
                    Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
                ).get(id=aerolinea_id)
    serializer = AerolineaSerializer(aerolinea)
    return Response(serializer.data)

#Obtener Aerolinea
@api_view(['GET']) 
def Aerolinea_obtener(request):
    aerolinea = Aerolinea.objects.prefetch_related(
                    Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
                    Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
                )
    serializer = AerolineaSerializer(aerolinea, many=True)
    return Response(serializer.data)

#Obtener Pasajeros
@api_view(['GET']) 
def Pasajeros_obtener(request):
    pasjero = Pasajero.objects.prefetch_related(
    Prefetch('vuelo'),                    # ManyToMany con Vuelo
    Prefetch('equipaje_pasajero'),        # ManyToOne con Equipaje
    Prefetch('reserva_pasajero'),         # ManyToOne con Reserva
    Prefetch('pajarelo_asiento'),         # ManyToOne con Asiento
).select_related('usuario')
    serializer = PasajeroSerializer(pasjero, many=True)  # ✅ Se añade many=True para manejar una lista
    return Response(serializer.data)

#Obtener Usuario por id
@api_view(['GET']) 
def Usuario_obtener(request,usuario_id):
    usuario = Usuario.objects.all().get(id=usuario_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

#Obtener Pasajeros
@api_view(['GET']) 
def Vuelo_obtener(request):
    vuelo = Vuelo.objects.prefetch_related(
    Prefetch('vuelo_pasajero'),           # ManyToMany con Pasajero
    Prefetch('asiento_vuelo'),            # ManyToOne con Asiento
    Prefetch('vuelo_media_aerolinea'),    # ManyToOne con VueloAerolinea
    Prefetch('vuelo_datos')               # OneToOne con EstadisticasVuelo
).select_related(
    'origen',                             # ManyToOne con Aeropuerto (origen)
    'destino'                             # ManyToOne con Aeropuerto (destino)
)
    serializer = VueloSerializer(vuelo, many=True)  # ✅ Se añade many=True para manejar una lista
    return Response(serializer.data)

#Obtener Reserva
@api_view(['GET']) 
def Vuelo_obtener_id(request,vuelo_id):
    vuelo = Vuelo.objects.prefetch_related(
    Prefetch('vuelo_pasajero'),           # ManyToMany con Pasajero
    Prefetch('asiento_vuelo'),            # ManyToOne con Asiento
    Prefetch('vuelo_media_aerolinea'),    # ManyToOne con VueloAerolinea
    Prefetch('vuelo_datos')               # OneToOne con EstadisticasVuelo
).select_related(
    'origen',                             # ManyToOne con Aeropuerto (origen)
    'destino'                             # ManyToOne con Aeropuerto (destino)
).get(id=vuelo_id)
    serializer = VueloSerializer(vuelo) 
    return Response(serializer.data)

#Obtener Reserva
@api_view(['GET']) 
def Reserva_obtener_id(request,reserva_id):
    reserva = Reserva.objects.select_related(
    'pasajero',
    'vuelo'
).get(id=reserva_id)
    serializer = ReservaSerializer(reserva) 
    return Response(serializer.data)

#Obtener Reserva
@api_view(['GET']) 
def Reserva_obtener(request):
    reserva = Reserva.objects.select_related(
    'pasajero',
    'vuelo'
)
    serializer = ReservaSerializer(reserva) 
    return Response(serializer.data)
#--------------------------------------Formularios_Crear----------------------------------------------------------------

@api_view(['POST'])
def Aeropuerto_create(request): 
    aeropuertoCreateSerializer = AeropuertoSerializerCreate(data=request.data)

    if aeropuertoCreateSerializer.is_valid():
        try:
            aeropuertoCreateSerializer.save()
            return Response("Aeropuerto Creado")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", aeropuertoCreateSerializer.errors)
        return Response(aeropuertoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Aerolinea_create(request): 
    aerolineaCreateSerializer = AerolineaSerializerCreate(data=request.data)

    if aerolineaCreateSerializer.is_valid():
        try:
            aerolineaCreateSerializer.save()
            return Response("Aerolinea Creado")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", aerolineaCreateSerializer.errors)
        return Response(aerolineaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Reserva_create(request): 
    reservaCreateSerializer = ReservaSerializerCreate(data=request.data)

    if reservaCreateSerializer.is_valid():
        try:
            reservaCreateSerializer.save()
            return Response("Reserva Creado")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", reservaCreateSerializer.errors)
        return Response(reservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Vuelo_create(request): 
    vueloCreateSerializer = VueloSerializerCreate(data=request.data)
    print("📩 Datos recibidos en la petición:", request.data)  # Depurar datos entrantes

    if vueloCreateSerializer.is_valid():
        try:
            vueloCreateSerializer.save()
            return Response("Vuelo Creado")
        
        except serializers.ValidationError as error:
            print("❌ Error de validación en el guardado:", error.detail)
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("🔥 Error inesperado:", repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", vueloCreateSerializer.errors)
        return Response(vueloCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#--------------------------------------Formularios_Editar----------------------------------------------------------------

@api_view(['PUT'])
def Aeropuerto_editar(request,aeropuerto_id):
    aeropuerto = Aeropuerto.objects.get(id=aeropuerto_id)
    AeropuertoCreateSerializer = AeropuertoSerializerCreate(data=request.data,instance=aeropuerto)
    if AeropuertoCreateSerializer.is_valid():
        try:
            AeropuertoCreateSerializer.save()
            #return Response({"mensaje": "✅ Aeropuerto editado correctamente."}, status=status.HTTP_200_OK)
            return Response("Aeropuerto EDITADO")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(AeropuertoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def Aerolinea_editar(request,aerolinea_id):
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 
    aerolinea = Aerolinea.objects.get(id=aerolinea_id)
    AerolineaCreateSerializer = AerolineaSerializerCreate(data=request.data,instance=aerolinea)
    if AerolineaCreateSerializer.is_valid():
        try:
            AerolineaCreateSerializer.save()
            #return Response({"mensaje": "✅ Aeropuerto editado correctamente."}, status=status.HTTP_200_OK)
            return Response("Aerolinea EDITADO")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(AerolineaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def Reserva_editar(request,reserva_id):
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 
    reserva = Reserva.objects.get(id=reserva_id)
    ReservaCreateSerializer = ReservaSerializerCreate(data=request.data,instance=reserva)
    if ReservaCreateSerializer.is_valid():
        try:
            ReservaCreateSerializer.save()
            return Response("Reserva EDITADO")
        
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(ReservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def Vuelo_editar(request, vuelo_id):
    print(f"📌 Datos recibidos en la API (JSON): {request.data}") 

    try:
        vuelo = Vuelo.objects.get(id=vuelo_id)
    except Vuelo.DoesNotExist:
        print(f"❌ ERROR: Vuelo con ID {vuelo_id} no encontrado")
        return Response({"error": "Vuelo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Serializador con instancia existente (edición)
    VueloCreateSerializer = VueloSerializerCreate(instance=vuelo, data=request.data)

    # 🔍 Depuración: Verificar si los datos pasan la validación
    if VueloCreateSerializer.is_valid():
        try:
            print(f"✅ Datos validados antes de guardar: {VueloCreateSerializer.validated_data}")  # Ver qué datos se guardarán
            VueloCreateSerializer.save()
            print("✔️ Vuelo editado exitosamente en la base de datos.")
            return Response("Vuelo EDITADO", status=status.HTTP_200_OK)

        except serializers.ValidationError as error:
            print(f"❌ ERROR en validación al guardar: {error.detail}")
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(f"🔥 ERROR inesperado al guardar: {repr(error)}")
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        print(f"❌ ERROR en validación: {VueloCreateSerializer.errors}")
        return Response(VueloCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
#--------------------------------------Formularios_Actualizar----------------------------------------------------------------

@api_view(['PATCH'])
def Aeropuerto_actualizar_nombre(request,aeropuerto_id):
    aeropuerto = Aeropuerto.objects.get(id=aeropuerto_id)
    serializers = AeropuertoSerializerActualizarNombre(data=request.data,instance=aeropuerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Aeropuerto Actualizada")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])    
def Aerolinea_actualizar_nombre(request,aerolinea_id):
    aerolinea = Aerolinea.objects.get(id=aerolinea_id)
    serializers = AerolineaSerializerActualizarNombre(data=request.data,instance=aerolinea)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Aerolinea Actualizada")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])    
def Reserva_actualizar_codigo(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    serializers = ReservaSerializerActualizarcodigo(data=request.data,instance=reserva)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Reserva Actualizada")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------Formularios_Eliminar----------------------------------------------------------------

@api_view(['DELETE'])
def Aeropuerto_eliminar(request,aeropuerto_id):
    aeropuerto = Aeropuerto.objects.get(id=aeropuerto_id)
    try:
        aeropuerto.delete()
        return Response("Aeropuerto ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def Aerolinea_eliminar(request,aerolinea_id):
    aerolinea = Aerolinea.objects.get(id=aerolinea_id)
    try:
        aerolinea.delete()
        return Response("Aerolinea ELIMINADA")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def Reserva_eliminar(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        return Response("Reserva ELIMINADA")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
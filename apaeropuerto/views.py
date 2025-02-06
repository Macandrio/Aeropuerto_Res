from django.shortcuts import render, redirect
from django.db.models import Prefetch, Q, Sum, Count
from .models import (
    Aeropuerto, Vuelo, Pasajero, Equipaje, Aerolinea, 
    VueloAerolinea, Reserva, Empleado, Asiento, Servicio ,ContactoAeropuerto , EstadisticasVuelo ,
)

from .forms import * # El * Coge todos los modelos es lo mismo que hacer lo de from .models import
from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.models import Group





def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    if (request.user.is_anonymous == False):       
        if(not "nombreusuario" in request.session):
            request.session["nombreusuario"] = request.user.username
        if(not "email" in request.session):
            request.session["email"] = request.user.email
        if(not "rol" in request.session):
            if (request.user.rol == 1):
                request.session["rol"] = "Administrador"
            elif (request.user.rol == 2):
                request.session["rol"] = "Pasajero"
            else:
                request.session["rol"] ="Gerente"
        if (not "grupo" in request.session):
            if (request.user.rol == 1):
                request.session["grupo"] = "Administrador"
            elif (request.user.rol == 2):
                request.session["grupo"] = "Pasajero"
            else:
                request.session["grupo"] ="Gerente" 
    return render(request, 'index.html')


#--------------------------------------------- Listas -----------------------------------------------------------------


# Vista para listar Aeropuertos
#@permission_required('apaeroperto.view_Aeropuerto')
def lista_aeropuerto(request):
    aeropuertos = Aeropuerto.objects.all()
    return render(request, 'paginas/aeropuerto_list.html', {'aeropuertos': aeropuertos})

# Vista para listar Vuelos
#@permission_required('apaeroperto.view_Vuelo')
def lista_vuelo(request):
    vuelos = Vuelo.objects.all()
    return render(request, 'paginas/vuelo_list.html', {'vuelos': vuelos})

# Vista para listar Pasajeros
@permission_required('apaeroperto.view_Pasajero')
def lista_pasajero(request):
    pasajeros = Pasajero.objects.all()
    return render(request, 'paginas/pasajero_list.html', {'pasajeros': pasajeros})

# Vista para listar Equipajes
@permission_required('apaeroperto.view_Equipaje')
def lista_equipaje(request):
    equipajes = Equipaje.objects.all()
    return render(request, 'paginas/equipaje_list.html', {'equipajes': equipajes})

# Vista para listar Aerolíneas
#@permission_required('apaeroperto.view_Aerolinea')
def lista_aerolineas(request):  # Cambiado aquí
    aerolineas = Aerolinea.objects.all()
    return render(request, 'paginas/aerolinea_list.html', {'aerolineas': aerolineas})

# Vista para listar VueloAerolinea
@permission_required('apaeroperto.view_VueloAerolinea')
def lista_vuelos_aerolineas(request):  # Cambiado aquí
    vuelos_aerolineas = VueloAerolinea.objects.all()
    return render(request, 'paginas/vuelo_aerolinea_list.html', {'vuelos_aerolineas': vuelos_aerolineas})

# Vista para listar Reservas
@permission_required('apaeroperto.view_Reserva')
def lista_reserva(request):
    reservas = Reserva.objects.all()
    return render(request, 'paginas/reserva_list.html', {'reservas': reservas})

# Vista para listar Empleados
@permission_required('apaeroperto.view_Empleado')
def lista_empleado(request):
    empleados = Empleado.objects.all()
    return render(request, 'paginas/empleado_list.html', {'empleados': empleados})

# Vista para listar Asientos
@permission_required('apaeroperto.view_Asiento')
def lista_silla(request):
    sillas = Asiento.objects.all()
    return render(request, 'paginas/silla_list.html', {'sillas': sillas})

# Vista para listar Servicios
@permission_required('apaeroperto.view_Servicio')
def lista_servicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'paginas/servicio_list.html', {'servicios': servicios})

# Vista para listar ContactoAeropuerto
@permission_required('apaeroperto.view_ContactoAeropuerto')
def lista_ContactoAeropuerto(request):
    contactoAero = ContactoAeropuerto.objects.all()
    return render(request, 'paginas/lista_ContactoAeropuerto_listar.html', {'contactoAero': contactoAero})

# Vista para listar EstadisticasVuelo
@permission_required('apaeroperto.view_EstadisticasVuelo')
def lista_EstadisticasVuelo(request):
    estadisticas = EstadisticasVuelo.objects.all()
    return render(request, 'paginas/estadisticas_list.html', {'estadisticas': estadisticas})


#--------------------------------------------- Consultas -----------------------------------------------------------------


# 1. Todos los pasajeros que esten asociados a un vuelo con una relación reversa

#@permission_required('apaeroperto.view_Vuelo')
def pasajeros_vuelo(request , id_vuelo):
    vuelo = Vuelo.objects.prefetch_related(Prefetch('vuelo_pasajero')).get(id=id_vuelo)
  
    return render(request, 'consultas/pasajeros_vuelo.html',{'vuelo': vuelo})
                         
# 2. Todos los vuelos que esten volando que esten una año en concreto

@permission_required('apaeroperto.view_EstadisticasVuelo')
def vuelo_volando_año(request , anyo):
    datosvuelo = EstadisticasVuelo.objects.select_related('vuelo')
    datosvuelo = datosvuelo.filter(fecha_estadisticas__year = anyo, vuelo__estado = False)

    return render(request, 'consultas/vuelo_volando_año.html',{'datosvuelo': datosvuelo})

# 3. feedbacks de todos los vuelos que tenga una palabra en concreto de una aerolinea en concreto desde la tabla intermedia

@permission_required('apaeroperto.view_Aerolinea')
def texto_vuelo_aerolinea(request, id_aerolinea, texto_buscar):
    
    aerolinea = Aerolinea.objects.get(id=id_aerolinea)

    vuelo_aerolinea = VueloAerolinea.objects.select_related('aerolinea','vuelo', 'vuelo__vuelo_datos')
    vuelo_aerolinea = vuelo_aerolinea.filter(aerolinea_id=id_aerolinea, vuelo__vuelo_datos__feedback_pasajeros__icontains=texto_buscar)
    return render(request, 'consultas/texto_vuelo_aerolinea.html', {'vuelo_aerolinea': vuelo_aerolinea, 'aerolinea': aerolinea})



# 4. Obtener el feedbacks de todos los vuelos en el que ha estado un pasajero específico.

@permission_required('apaeroperto.view_Pasajero')
def historial_feedbacks_pasajero(request, pasajero_id):

    pasajero = Pasajero.objects.get(id=pasajero_id) # Obtener el pasajero

    feedbacks = EstadisticasVuelo.objects.select_related('vuelo')
    feedbacks = feedbacks.filter(vuelo__vuelo_pasajero=pasajero)
    return render(request, 'consultas/historial_feedbacks_pasajero.html', {'feedbacks': feedbacks, 'pasajero': pasajero})


#5. Obtener todos los vuelos que salgan desde un aeropuerto específico y lleguen a un destino específico

#@permission_required('apaeroperto.view_Vuelo')
def vuelos_origen_destino(request, origen_id, destino_id):
    
    vuelos = Vuelo.objects.select_related('origen', 'destino') 
    vuelos = vuelos.filter(origen_id=origen_id, destino_id=destino_id)

    return render(request, 'consultas/vuelos_origen_destino.html', {'vuelos': vuelos})


#6. Listar reservas por método de pago y año

@permission_required('apaeroperto.view_Reserva')
def reservas_por_metodo_y_año(request, metodo_pago, año):
    reservas = Reserva.objects.select_related('pasajero', 'vuelo')
    reservas = reservas.filter(metodo_pago=metodo_pago,fecha_reserva__year=año)

    return render(request, 'consultas/reservas_por_metodo_y_año.html', {'reservas': reservas})


# 7. Obtener todos los vuelos que tengan un origen y destino en concreto o que el estado sea volando

#@permission_required('apaeroperto.view_Vuelo')
def vuelos_cortos_origen_destino(request, origen_id, destino_id, estado):

    vuelos = Vuelo.objects.select_related('origen', 'destino')
    vuelos = vuelos.filter(Q(origen_id=origen_id) & Q(destino_id=destino_id) | (~Q(estado=estado)))

    return render(request, 'consultas/vuelos_cortos.html', {'vuelos': vuelos})



# 8. Calcular el peso total del equipaje de todos los pasajeros en un vuelo específico y ordenar

@permission_required('apaeroperto.view_Equipaje')
def peso_equipaje_vuelo(request, vuelo_id):
    
    equipajes = Equipaje.objects.select_related('pasajero')
    equipajes = equipajes.filter(pasajero__vuelo__id=vuelo_id).order_by('-peso')[:5] 
    peso_total = equipajes.aggregate(Sum('peso'))['peso__sum']  

    return render(request, 'consultas/peso_equipaje_vuelo.html', {'equipajes': equipajes,'peso_total': peso_total})

# 9. Listar todos los vuelos de una aerolínea específica que no tienen registrada una fecha de operación en la tabla intermedia

@permission_required('apaeroperto.view_VueloAerolinea')
def vuelos_sin_operacion(request, aerolinea_id):

    vuelos = VueloAerolinea.objects.select_related('aerolinea', 'vuelo')
    vuelos = vuelos.filter(aerolinea_id=aerolinea_id, fecha_operacion__isnull=True)

    return render(request, 'consultas/vuelos_sin_operacion.html', {'vuelos': vuelos})



# 10. Calcular cuantos pasajeros hay en un vuelo

@permission_required('apaeroperto.view_Pasajero')
def cuantos_pasajeros_vuelo(request, id_vuelo):
    
    pasajeros = Pasajero.objects.prefetch_related('vuelo')
    pasajeros = pasajeros.filter(vuelo__id=id_vuelo)
    total_pasajeros = pasajeros.aggregate(Count('id'))['id__count']
    
    return render(request, 'consultas/total_pasajeros.html', {'total_pasajeros': total_pasajeros, 'pasajeros': pasajeros})

#----------------------------------------------------------------------- Formulario -----------------------------------------------------------------

# Formulario Aeropuerto


@permission_required('apaeropuerto.add_Aeropuerto')
def crear_aeropuerto(request):
    if request.method == "POST":
        formulario = AeropuertoForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "El aeropuerto se creó exitosamente.")
                return redirect("Aeropuerto_buscar_avanzado")
            except Exception as error:
                messages.error(request, f"Error inesperado al guardar el aeropuerto: {error}")
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, "Ya existe un aeropuerto con el mismo nombre. Verifica los datos ingresados.")
    else:
        formulario = AeropuertoForm()

    return render(request, 'Formularios/Aeropuerto/crear_aeropuerto.html', {"formulario": formulario})


@permission_required('apaeropuerto.view_Aeropuerto') 
def Aeropuerto_buscar_avanzado(request):
    
    if len(request.GET) > 0:
        
        formulario = BusquedaAvanzadaAeropuertoForm(request.GET)
        
        if formulario.is_valid():
            aeropuerto = Aeropuerto.objects.prefetch_related(
                Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
                Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
                Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
                Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
            )

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            ciudades = formulario.cleaned_data.get('ciudades')
            pais = formulario.cleaned_data.get('pais')

            if textoBusqueda:
                aeropuerto = aeropuerto.filter(nombre__icontains=textoBusqueda)

            if ciudades:
                aeropuerto = aeropuerto.filter(ciudades=ciudades)

            if pais:
                aeropuerto = aeropuerto.filter(pais= pais)
        else:
            return render (request, 'Formularios/Aeropuerto/busqueda_avanzada.html', {
                'formulario': formulario,
                'aeropuerto': []
            })
    else:
        formulario = BusquedaAvanzadaAeropuertoForm(None)
        aeropuerto = Aeropuerto.objects.all()
        
    return render (request, 'Formularios/Aeropuerto/busqueda_avanzada.html', {
        'formulario': formulario,
        'aeropuerto': aeropuerto
    })


@permission_required('apaeropuerto.change_Aeropuerto') 
def editar_aeropuerto(request, aeropuerto_id):
    aeropuerto = Aeropuerto.objects.get(id=aeropuerto_id)  # Obtiene el aeropuerto por ID

    if request.method == 'POST':
        formulario = AeropuertoForm(request.POST, instance=aeropuerto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha editado el Aeropuerto '+formulario.cleaned_data.get('nombre')+" correctamente")
            return redirect('Aeropuerto_buscar_avanzado')  # Redirige a la lista después de actualizar
    else:
        formulario = AeropuertoForm(instance=aeropuerto)

    return render(request, 'Formularios/Aeropuerto/editar_aeropuerto.html', {'formulario': formulario, 'aeropuerto': aeropuerto})


@permission_required('apaeropuerto.delete_Aeropuerto')
def eliminar_aeropuerto(request, aeropuerto_id):
    aeropuerto = Aeropuerto.objects.get(id=aeropuerto_id)
    if request.method == 'POST':
        aeropuerto.delete()
        return redirect('Aeropuerto_buscar_avanzado')  # Redirige a la lista después de eliminar
    return render(request, 'Formulario/Aeropuerto/eliminar_aeropuerto.html', {'aeropuerto': aeropuerto})

  
    
# Formulario contacto_Aeropuerto


@permission_required('apaeropuerto.add_ContactoAeropuerto')
def crear_contacto(request): 
    if (request.method == "POST"):
        formulario=ContactoAeropuertoform(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "El contacto se creó exitosamente.")
                return redirect("contacto_Aeropuerto_buscar_avanzado")
            except Exception as error:
                print(error)
    else:
        formulario=ContactoAeropuertoform()  
    return render(request,'Formularios/Contacto_Aeropuerto/crear_Contacto.html',{"formulario":formulario})


@permission_required('apaeropuerto.view_ContactoAeropuerto') 
def contacto_Aeropuerto_buscar_avanzado(request):
    
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaContacto(request.GET)
        
        if formulario.is_valid():
            contactos = ContactoAeropuerto.objects.select_related('aeropuerto')

            nombre_contacto = formulario.cleaned_data.get('nombre_contacto')
            telefono_contacto = formulario.cleaned_data.get('telefono_contacto')
            años_trabajados = formulario.cleaned_data.get('años_trabajados')

            if nombre_contacto:
                contactos = contactos.filter(nombre_contacto__icontains=nombre_contacto)

            if telefono_contacto:
                contactos = contactos.filter(telefono_contacto=telefono_contacto)

            if años_trabajados:
                contactos = contactos.filter(años_trabajados= años_trabajados)

            contactos = contactos.all()
        else:
            return render (request, 'Formularios/Contacto_Aeropuerto/busqueda_avanzada.html', {
                'formulario': formulario,
                'contactos': []
            })
    else:
        formulario = BusquedaAvanzadaContacto(None)
        contactos = ContactoAeropuerto.objects.all()
    return render (request, 'Formularios/Contacto_Aeropuerto/busqueda_avanzada.html', {
        'formulario': formulario,
        'contactos': contactos
    })


@permission_required('apaeropuerto.change_ContactoAeropuerto') 
def contacto_Aeropuert_modificar(request,contacto_id):
    contacto = ContactoAeropuerto.objects.get(id=contacto_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = ContactoAeropuertoform(datosFormulario,instance = contacto)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el Contacto '+formulario.cleaned_data.get('nombre_contacto')+" correctamente")
                return redirect('contacto_Aeropuerto_buscar_avanzado')  
            except Exception as error:
                print(error)
    return render(request, 'Formularios/Contacto_Aeropuerto/modificar.html',{"formulario":formulario,"contacto":contacto})


@permission_required('apaeropuerto.delete_ContactoAeropuerto')
def contacto_Aeropuert_eliminar(request,contacto_id):
    contacto = ContactoAeropuerto.objects.get(id=contacto_id)
    try:
        contacto.delete()
        messages.success(request, "Se ha elimnado el contacto "+contacto.nombre_contacto+" correctamente")
    except Exception as error:
        print(error)
    return redirect('contacto_Aeropuerto_buscar_avanzado')



# Formulario estadisticasvuelo


#@permission_required('apaeropuerto.add_EstadisticasVuelo')
def crear_estadisticasvuelo(request): 
    if (request.method == "POST"):
        formulario=estadisticasvueloform(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "La Estasdistica se creó exitosamente.")
                return redirect("Estadisticas_buscar_avanzado")
            except Exception as error:
                print(error)
    else:
        formulario=estadisticasvueloform()  
    return render(request,'Formularios/Estadisticas_vuelo/crear_Estadisticasvuelo.html',{"formulario":formulario})


#@permission_required('apaeropuerto.view_add_EstadisticasVuelo') 
def Estadisticas_buscar_avanzado(request):    

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEstadisticas(request.GET)
        
        if formulario.is_valid():
            estadisticas = EstadisticasVuelo.objects.select_related('vuelo')
            fecha_estadisticas = formulario.cleaned_data.get('fecha_estadisticas')
            numero_asientos_vendidos = formulario.cleaned_data.get('numero_asientos_vendidos')
            numero_cancelaciones = formulario.cleaned_data.get('numero_cancelaciones')

            if fecha_estadisticas:
                estadisticas = estadisticas.filter(fecha_estadisticas=fecha_estadisticas)

            if numero_asientos_vendidos:
                estadisticas = estadisticas.filter(numero_asientos_vendidos=numero_asientos_vendidos)

            if numero_cancelaciones:
                estadisticas = estadisticas.filter(numero_cancelaciones = numero_cancelaciones)
        else:
            return render (request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {
                'formulario': formulario,
                'estadisticas': [],
            })
    else:
        formulario = BusquedaAvanzadaEstadisticas(None)
        estadisticas = EstadisticasVuelo.objects.all()

    return render (request, 'Formularios/Estadisticas_vuelo/busqueda_avanzada.html', {
        'formulario': formulario,
        'estadisticas': estadisticas,
    })


#@permission_required('apaeropuerto.change_EstadisticasVuelo')
def Estadisticas_modificar(request,estadisticas_id):
    estadisticas = EstadisticasVuelo.objects.get(id=estadisticas_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = estadisticasvueloform(datosFormulario,instance = estadisticas)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la estadisticas de la fecha'+formulario.cleaned_data.get('fecha_estadisticas')+" correctamente")
                return redirect('Estadisticas_buscar_avanzado')  
            except Exception as error:
                print(error)
    return render(request, 'Formularios/Estadisticas_vuelo/modificar.html',{"formulario":formulario,"estadisticas":estadisticas})


#@permission_required('apaeropuerto.delete_EstadisticasVuelo')
def Estadisticas_eliminar(request,estadisticas_id):
    estadisticas = EstadisticasVuelo.objects.get(id=estadisticas_id)
    try:
        estadisticas.delete()
        messages.success(request, "Se ha elimnado la estadistica "+estadisticas.id+" correctamente")
    except Exception as error:
        print(error)
    return redirect('Estadisticas_buscar_avanzado')



# Formulario Aerolinea


@permission_required('apaeropuerto.add_Aerolinea')
def crear_Aerolinea(request): 
    if (request.method == "POST"):
        formulario=Aerolineaform(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "La Aerolinea se creó exitosamente.")
                return redirect("Aerolinea_buscar_avanzado")
            except Exception as error:
                print(error)
    else:
        formulario=Aerolineaform()  
    return render(request,'Formularios/Aerolinea/crear_aerolinea.html',{"formulario":formulario})


@permission_required('apaeropuerto.view_add_Aerolinea') 
def Aerolinea_buscar_avanzado(request):

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAerolinea(request.GET)
        
        if formulario.is_valid():
            aerolineas = Aerolinea.objects.prefetch_related(
                                                            Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
                                                            Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
                                                        )

            nombre = formulario.cleaned_data.get('nombre')
            codigo = formulario.cleaned_data.get('codigo')
            pais = formulario.cleaned_data.get('pais')

            if nombre:
                aerolineas = aerolineas.filter(nombre__icontains=nombre)

            if codigo:
                aerolineas = aerolineas.filter(codigo=codigo)

            if pais:
                aerolineas = aerolineas.filter(pais = pais)
        else:
            return render (request, 'Formularios/Aerolinea/buscar.html', {
                'formulario': formulario,
                'aerolineas': []
            })
    else:
        formulario = BusquedaAvanzadaAerolinea(None)
        aerolineas = Aerolinea.objects.all()


    return render (request, 'Formularios/Aerolinea/buscar.html', {
        'formulario': formulario,
        'aerolineas': aerolineas
    })


@permission_required('apaeropuerto.change_Aerolinea')
def Aerolinea_modificar(request,aerolinea_id):
    aerolinea = Aerolinea.objects.get(id=aerolinea_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = Aerolineaform(datosFormulario,instance = aerolinea)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el aerolinea '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('Aerolinea_buscar_avanzado')  
            except Exception as error:
                print(error)
    return render(request, 'Formularios/Aerolinea/modificar.html',{"formulario":formulario,"aerolinea":aerolinea})


@permission_required('apaeropuerto.delete_Aerolinea')
def Aerolinea_eliminar(request,aerolinea_id):
    aerolinea = Aerolinea.objects.get(id=aerolinea_id)
    try:
        aerolinea.delete()
        messages.success(request, "Se ha elimnado el contacto "+aerolinea.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('Aerolinea_buscar_avanzado')



# Formulario Vuelo


@permission_required('apaeropuerto.add_Vuelo')
def crear_Vuelo(request): 
    if (request.method == "POST"):
        formulario=VueloForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "El vuelo se creó exitosamente.")
                return redirect("Vuelo_buscar_avanzado")
            except Exception as error:
                messages.error(request, f"Error inesperado al guardar el aeropuerto: {error}")
    else:
        formulario=VueloForm()  
    return render(request,'Formularios/Vuelo/crear_vuelo.html',{"formulario":formulario})


@permission_required('apaeropuerto.view_add_Vuelo') 
def Vuelo_buscar_avanzado(request):
    formulario = BusquedaAvanzadaVuelo(request.GET)
    vuelos = Vuelo.objects.all()
    aeropuerto = Aeropuerto.objects.all()

    if len(request.GET) > 0:
        if formulario.is_valid():
            hora_salida = formulario.cleaned_data.get('hora_salida')
            hora_llegada = formulario.cleaned_data.get('hora_llegada')
            estado = formulario.cleaned_data.get('estado')
            origen = formulario.cleaned_data.get('origen')
            destino = formulario.cleaned_data.get('destino')


            if hora_salida:
                vuelos = vuelos.filter(hora_salida=hora_salida)

            if hora_llegada:
                vuelos = vuelos.filter(hora_llegada=hora_llegada)

            if estado:
                vuelos = vuelos.filter(estado=estado)

            if origen:
                vuelos = vuelos.filter(origen = origen)

            if destino:
                vuelos = vuelos.filter(destino = destino)

        else:
            return render (request, 'Formularios/Vuelo/buscar.html', {
                'formulario': formulario,
                'vuelos': [],
                'aeropuerto': aeropuerto
            })

    return render (request, 'Formularios/Vuelo/buscar.html', {
        'formulario': formulario,
        'vuelos': vuelos,
        'aeropuerto': aeropuerto
    })


@permission_required('apaeropuerto.change_Vuelo')
def Vuelo_modificar(request,vuelo_id):
    vuelo = Vuelo.objects.get(id=vuelo_id)
    
    if request.method == "POST":
        formulario = VueloForm(request.POST, instance=vuelo_id)
        if formulario.is_valid():  
            formulario.save()
            messages.success(request, 'Se ha editado el vuelo '+formulario.cleaned_data.get('id')+" correctamente")
            return redirect('Vuelo_buscar_avanzado')  
    else:
        formulario = VueloForm(instance=vuelo)
    return render(request, 'Formularios/Vuelo/modificar.html',{"formulario":formulario,"vuelo":vuelo})


@permission_required('apaeropuerto.delete_Vuelo')
def Vuelo_eliminar(request,vuelo_id):
    vuelo = Vuelo.objects.get(id=vuelo_id)
    try:
        vuelo.delete()
        messages.success(request, "Se ha elimnado el vuelo "+vuelo.id+" correctamente")
    except Exception as error:
        print(error)
    return redirect('Vuelo_buscar_avanzado')



#Formulario Pasajero


@permission_required('apaeropuerto.add_Pasajero')
def crear_pasajero(request): 
    if (request.method == "POST"):
        formulario=PasajeroForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("Pasajero_buscar_avanzado")
            except Exception as error:
                print(error)
    else:
        formulario=PasajeroForm    
    return render(request,'Formularios/Pasajero/crear_pasajero.html',{"formulario":formulario})


@permission_required('apaeropuerto.view_add_Pasajero') 
def Pasajero_buscar_avanzado(request):

    if request.GET:
        formulario = BusquedaAvanzadaPasajero(request.GET)
        pasajeros = Pasajero.objects.all()
    
        if formulario.is_valid():
            dni = formulario.cleaned_data.get('dni')
            direccion = formulario.cleaned_data.get('apellido')

            if direccion:
                pasajeros = pasajeros.filter(nombre__icontains=direccion)

            if dni:
                pasajeros = pasajeros.filter(telefono = dni)
        else:
            return render (request, 'Formularios/Pasajero/buscar.html', {
                'formulario': formulario,
                'pasajeros': []
            })
    else:
        formulario = BusquedaAvanzadaPasajero(None)
        pasajeros = Pasajero.objects.all()
    

    return render (request, 'Formularios/Pasajero/buscar.html', {
        'formulario': formulario,
        'pasajeros': pasajeros,
    })


@permission_required('apaeropuerto.change_Pasajero')
def Pasajero_modificar(request,pasajero_id):
    pasajero = Pasajero.objects.get(id=pasajero_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = PasajeroForm(datosFormulario,instance = pasajero)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el pasajero '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('Pasajero_buscar_avanzado')  
            except Exception as error:
                print(error)
    return render(request, 'Formularios/Pasajero/modificar.html',{"formulario":formulario,"pasajero":pasajero})


@permission_required('apaeropuerto.delete_Pasajero')
def Pasajero_eliminar(request,pasajero_id):
    pasajero = Pasajero.objects.get(id=pasajero_id)
    try:
        pasajero.delete()
        messages.success(request, "Se ha elimnado el pasajero "+pasajero.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('Pasajero_buscar_avanzado')



#Reservas


#@permission_required('apaeropuerto.add_Reserva')
def crear_reserva(request):

    pasajero = Pasajero.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)  # No guarda la instancia aún
            reserva.pasajero = pasajero  # Asigna el pasajero al campo
            reserva.save()  # Guarda la reserva en la base de datos
            messages.success(request, "Reserva creada correctamente.")
            return redirect('Reserva_buscar_avanzado')
    else:
        form = ReservaForm()

    return render(request, 'Formularios/Reservas/crear.html', {'form': form})


#@permission_required('apaeropuerto.view_add_Reserva') 
def Reserva_buscar_avanzado(request):

    pasajero_logueado = Pasajero.objects.get(usuario=request.user)

    reservas = Reserva.objects.filter(pasajero=pasajero_logueado)  # Filtra por pasajero logueado

    if request.GET:
        formulario = BusquedaAvanzadaReservaForm(request.GET)
        
        if formulario.is_valid():
            fecha_reserva = formulario.cleaned_data.get('fecha_reserva')
            codigo_descueto = formulario.cleaned_data.get('codigo_descueto')
            metodo_pago = formulario.cleaned_data.get('metodo_pago')
            estado_de_pago = formulario.cleaned_data.get('estado_de_pago')

            # Aplica los filtros adicionales al queryset
            if fecha_reserva:
                reservas = reservas.filter(fecha_reserva=fecha_reserva)
            
            if codigo_descueto:
                reservas = reservas.filter(codigo_descueto__icontains=codigo_descueto)
            
            if metodo_pago:
                reservas = reservas.filter(metodo_pago=metodo_pago)
            
            if estado_de_pago is not None:
                reservas = reservas.filter(estado_de_pago=estado_de_pago)
        else:
            reservas = []  # Si el formulario no es válido, no se muestran resultados
    else:
        formulario = BusquedaAvanzadaReservaForm()

    return render(request, 'Formularios/Reservas/buscar.html', {
        'formulario': formulario,
        'reservas': reservas,
    })


#@permission_required('apaeropuerto.change_Reserva')
def editar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)  # Obtener la reserva por ID

    if request.method == 'POST':
        formulario = ReservaForm(request.POST, instance=reserva)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f"Reserva {reserva.id} actualizada correctamente.")
            return redirect('Reserva_buscar_avanzado')  # Redirigir tras la edición
        else:
            messages.error(request, "Error al actualizar la reserva. Verifica los datos.")
    else:
        formulario = ReservaForm(instance=reserva)

    return render(request, 'Formularios/Reservas/modificar.html', {
        'formulario': formulario,
        'reserva': reserva,
    })


#@permission_required('apaeropuerto.delete_Reserva')
def reserva_eliminar(request,reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        messages.success(request, "Se ha elimnado el pasajero "+reserva.id+" correctamente")
    except Exception as error:
        print(error)
    return redirect('Reserva_buscar_avanzado')




#--------------------------------------------- Usuario -----------------------------------------------------------------


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if(rol == Usuario.PASAJERO):
                grupo = Group.objects.get(name='Pasajero')
                grupo.user_set.add(user)
                pasajero = Pasajero.objects.create(usuario = user)
                pasajero.save()
            elif(rol == Usuario.GERENTE):
                grupo = Group.objects.get(name='Gerente')
                grupo.user_set.add(user)
                empleado = Gerente.objects.create(usuario = user)
                empleado.save()
            
            login(request, user)
            return redirect('index')

    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})



#--------------------------------------------- Errores -----------------------------------------------------------------

# Error 400 - Solicitud Incorrecta
def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

# Error 403 - Prohibido
def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

# Error 404 - No Encontrado
def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

# Error 500 - Error Interno del Servidor
def error_500(request):
    return render(request, 'errors/500.html', status=500)






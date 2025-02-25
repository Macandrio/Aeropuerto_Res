from rest_framework import serializers
from .models import *
from .forms import *
from datetime import datetime

#---------------------------------------------------------Modelos--------------------------------------------------------------------------------

#clase Aeropuerto

class AeropuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aeropuerto
        fields = '__all__'

# Clase Aerolinea

class AerolineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aerolinea
        fields = '__all__'

# clase Vuelo

class VueloSerializer(serializers.ModelSerializer):
   
    #Para relaciones ManyToOne o OneToOne
    origen = AeropuertoSerializer()

    destino = AeropuertoSerializer()
    
    #Para las relaciones ManyToMany
    aerolinea = AerolineaSerializer(read_only=True, many=True)
    
    #Para formatear Fechas
    hora_salida = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))

    #Para formatear Fechas
    hora_llegada = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    
    class Meta:
        fields = ('id',
                  'hora_salida',
                  'hora_llegada',
                  'estado',
                  'duracion',
                  'origen',
                  'destino',
                  'aerolinea'
                  )
        model = Vuelo

# Clase Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

# Clae Pasajero

class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = '__all__'

# clase Reserva
class ReservaSerializer(serializers.ModelSerializer):
   
    fecha_reserva = serializers.DateTimeField()
    codigo_descueto = serializers.CharField()
    metodo_pago = serializers.ChoiceField(choices=Reserva.METODO_PAGO_CHOICES)
    estado_de_pago = serializers.BooleanField()
    pasajero = PasajeroSerializer()
    vuelo =VueloSerializer()

    class Meta:
        fields = ('id',
                  'fecha_reserva',
                  'codigo_descueto',
                  'metodo_pago',
                  'estado_de_pago',
                  'pasajero',
                  'vuelo'
                  )
        model = Reserva


# clase VueloAerolionea
class VueloAerolineaSerializer(serializers.ModelSerializer):
   
    estado = serializers.CharField()
    fecha_operacion = serializers.DateTimeField()
    clase = serializers.ChoiceField(choices=VueloAerolinea.tipos_clase_avion)
    incidencias = serializers.CharField()
    vuelo =  VueloSerializer()
    aerolinea = AerolineaSerializer()

    class Meta:
        fields = ('id',
                  'estado',
                  'fecha_operacion',
                  'clase',
                  'incidencias',
                  'vuelo',
                  'aerolinea',
                  )
        model = VueloAerolinea


# clase Estadisticas
class EstadisticasSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticasVuelo
        fields = '__all__'

#---------------------------------------------------------Crear--------------------------------------------------------------------------------

# Aeropuerto
class  AeropuertoSerializerCreate(serializers.ModelSerializer):
    
    PAISES_OPCIONES = [("", "Ninguno")] + Aeropuerto.PAISES

    pais = serializers.ChoiceField(choices=PAISES_OPCIONES)

    CIUDADES_OPCIONES = [("", "Ninguno")] + Aeropuerto.CIUDADES

    ciudades = serializers.ChoiceField(choices=CIUDADES_OPCIONES)

    class Meta:
        model = Aeropuerto
        fields = '__all__'


    def validate_nombre(self,nombre):
        existe_nombre = Aeropuerto.objects.filter(nombre=nombre).first()

        if(not existe_nombre is None):
            if(not self.instance is None and existe_nombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un Aeropuerto con ese nombre')

            if len(nombre) < 0:
                raise serializers.ValidationError('Al menos debes indicar 1 caracteres')            
            
        return nombre
    
    def validate_ciudades(self,ciudades):
        if ciudades == "":
            raise serializers.ValidationError('Debes seleccionar una ciudad')
        return ciudades
    
    def validate_pais(self,pais):
        if pais == "":
            raise serializers.ValidationError('Debes seleccionar un pais')
        return pais
    
    def validate_capacidad_maxima(self,capacidad_maxima):
        if capacidad_maxima < 150:
            raise serializers.ValidationError('Debes tener una capacidad de 150 pasajeros como minimo')
        return capacidad_maxima
    
# Aerolinea
class  AerolineaSerializerCreate(serializers.ModelSerializer):
    
    PAISES_OPCIONES = [("", "Ninguno")] + Aerolinea.paises

    pais = serializers.ChoiceField(choices=PAISES_OPCIONES)

    class Meta:
        model = Aerolinea
        fields = '__all__'


    def validate_nombre(self,nombre):
        existe_nombre = Aerolinea.objects.filter(nombre=nombre).first()

        if(not existe_nombre is None):
            if(not self.instance is None and existe_nombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un Aerolinea con ese nombre')

            if len(nombre) < 0:
                raise serializers.ValidationError('Al menos debes indicar 1 caracteres')            
            
        return nombre
    
    def validate_pais(self,pais):
        if pais == "":
            raise serializers.ValidationError('Debes seleccionar un pais')
        return pais
    
    def validate_aeropuerto(self,aeropuerto): 
        if len(aeropuerto) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos un Aeropuerto')
        return aeropuerto

# Reserva
class  ReservaSerializerCreate(serializers.ModelSerializer):
    
    PAGO_OPCIONES = [("", "Ninguno")] + Reserva.METODO_PAGO_CHOICES

    metodo_pago = serializers.ChoiceField(choices=PAGO_OPCIONES)

    class Meta:
        model = Reserva
        fields = '__all__'

    
    def validate_metodo_pago(self,metodo_pago):
        if metodo_pago == "":
            raise serializers.ValidationError('Debes seleccionar un metodo de pago')
        return metodo_pago
    
    def validate_codigo_descueto(self,codigo_descueto): 
        if len(codigo_descueto) < 2:
            raise serializers.ValidationError('Debe tener al menos 1 caracter')
        return codigo_descueto
    
    def validate_fecha_reserva(self,fecha_reserva):
        hoy = datetime.datetime.now()
        if fecha_reserva < hoy:
            raise serializers.ValidationError("La fecha de reserva no puede ser anterior a la fecha actual.")
        return fecha_reserva
    
    def validate_vuelo(self,vuelo):
        if vuelo == "":
            raise serializers.ValidationError("Debes elegir un vuelo.")
        return vuelo
    
    def validate_pasajero(self,pasajero):
        if pasajero == "":
            raise serializers.ValidationError("Debes elegir un pasajero.")
        return pasajero

# Vuelo
class  VueloSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Vuelo
        fields = ['hora_salida','hora_llegada','estado','origen','destino','aerolinea']

    
    def validate_hora_llegada(self, hora_llegada):
        hora_salida = self.initial_data.get('hora_salida')  # Obtiene hora_salida del request

        if hora_salida and hora_llegada:  # Verifica que ambas fechas existen
            # Manejar distintos formatos de fecha/hora
            formatos_permitidos = [
                "%Y-%m-%dT%H:%M",      # Formato sin segundos (ej. '2025-02-18T13:35')
                "%Y-%m-%d %H:%M",      # Mismo pero con espacio en vez de 'T'
                "%Y-%m-%dT%H:%M:%S",   # Formato estándar con segundos
                "%Y-%m-%d %H:%M:%S"    # Espacio en vez de 'T'
            ]

            def convertir_fecha(fecha):
                if isinstance(fecha, str):
                    for formato in formatos_permitidos:
                        try:
                            return datetime.strptime(fecha, formato)
                        except ValueError:
                            continue
                    raise serializers.ValidationError(f"Formato de fecha/hora inválido: {fecha}")

                return fecha  # Ya es datetime

            hora_salida = convertir_fecha(hora_salida)
            hora_llegada = convertir_fecha(hora_llegada)

            # Validar que la hora de salida no sea mayor que la de llegada
            if hora_salida > hora_llegada:
                raise serializers.ValidationError('La hora de llegada debe ser después de la de salida')

        return hora_llegada
    
    def validate_origen(self, origen):
        destino_id = self.initial_data.get("destino")  # Obtiene el ID del destino desde el request

        if not destino_id or not origen:  # Verifica que ambos existan
            return origen

        if isinstance(origen, str):  # Si 'origen' es un nombre, obtenemos su ID
            origen_id = Vuelo.objects.filter(origen=origen).values_list("id", flat=True).first()
        else:
            origen_id = origen.id  # Si 'origen' ya es un objeto, usamos su ID directamente

        # Comparar IDs en lugar de nombres
        if int(destino_id) == origen_id:
            raise serializers.ValidationError("El origen debe ser distinto del destino.")

        return origen

    def validate_destino(self, destino):
        origen_id = self.initial_data.get("origen")  # Obtiene el ID del origen desde el request

        if not origen_id or not destino:  # Verifica que ambos existan
            return destino

        if isinstance(destino, str):  # Si 'destino' es un nombre, obtenemos su ID
            destino_id = Vuelo.objects.filter(destino=destino).values_list("id", flat=True).first()
        else:
            destino_id = destino.id  # Si 'destino' ya es un objeto, usamos su ID directamente

        # Comparar IDs en lugar de nombres
        if int(origen_id) == destino_id:
            raise serializers.ValidationError("El destino debe ser distinto del origen.")

        return destino

    
    def create(self, validated_data):
        aerolineas = self.initial_data.get("aerolinea", [])  # ✅ Forma correcta

        if len(aerolineas)<2:
            raise serializers.ValidationError({"aerolinea": ["Debe seleccionar al menos dos aerolínea"]})
        
        vuelo = Vuelo.objects.create(
            hora_salida = validated_data['hora_salida'],
            hora_llegada = validated_data['hora_llegada'],
            estado = validated_data['estado'],
            origen = validated_data['origen'],
            destino = validated_data['destino'],
        )

        vuelo.aerolinea.set(Aerolinea.objects.filter(id__in=aerolineas))

        return vuelo
    
    def update(self, instance, validated_data):
        aerolineas = self.initial_data.get("aerolinea", [])  # 🛠️ Extrae IDs de aerolíneas

        # ❌ Valida que al menos haya un vuelo y una aerolínea
        if len(aerolineas)<2:
            raise serializers.ValidationError({"aerolinea": ["Debe seleccionar al menos dos aerolínea"]})
        

        # ✅ Actualiza los campos normales
        instance.hora_salida = validated_data["hora_salida"]
        instance.hora_llegada = validated_data["hora_llegada"]
        instance.estado = validated_data["estado"]
        instance.origen = validated_data["origen"]
        instance.destino = validated_data["destino"]
        instance.save()

        instance.aerolinea.set(Aerolinea.objects.filter(id__in=aerolineas))

        return instance

        

    
#---------------------------------------------------------Actualizar--------------------------------------------------------------------------------

# Aeropuerto

class AeropuertoSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Aeropuerto
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        Nombre = Aeropuerto.objects.filter(nombre=nombre).first()
        if(not Nombre is None and Nombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un Aeropuerto con ese nombre')
        return nombre
    
# Aerolinea
class AerolineaSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Aerolinea
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        Nombre = Aerolinea.objects.filter(nombre=nombre).first()
        if(not Nombre is None and Nombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un Aeropuerto con ese nombre')
        return nombre

# Reserva  
class ReservaSerializerActualizarcodigo(serializers.ModelSerializer):
 
    class Meta:
        model = Reserva
        fields = ['codigo_descueto']
    
    def validate_codigo_descueto(self,codigo_descueto): 
        if len(codigo_descueto) < 2:
            raise serializers.ValidationError('Debe tener al menos 1 caracter')
        return codigo_descueto
    
# Vuelo  
class VueloSerializerActualizarestado(serializers.ModelSerializer):

    class Meta:
        model = Vuelo
        fields = ['hora_llegada']

    def validate_hora_llegada(self, hora_llegada):
        # Obtener la instancia actual del vuelo
        vuelo = self.instance  # Esto obtiene el vuelo que se está actualizando

        if vuelo and vuelo.hora_salida:  # Asegurar que el vuelo tiene hora_salida
            if hora_llegada <= vuelo.hora_salida:
                raise serializers.ValidationError("La hora de llegada debe ser después de la hora de salida.")

        return hora_llegada


#---------------------------------------------------------usuario--------------------------------------------------------------------------------

class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username
    
    def validate_password1(self, password1):
        password2 = self.initial_data.get("password2")  # Obtener password2 de los datos iniciales

        if password2 is None:
                raise serializers.ValidationError("Debe proporcionar el campo password2.")

        if password1 != password2:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return password1

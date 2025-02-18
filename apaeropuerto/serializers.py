from rest_framework import serializers
from .models import *
from .forms import *
import datetime


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
    hora_salida = serializers.DateTimeField()
    #Para formatear Fechas
    hora_llegada = serializers.DateTimeField()
    
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

# Vuelo Aerolineas
class  VueloAerolineasSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = VueloAerolinea
        fields = ['fecha_operacion','estado','clase','incidencias','vuelo','aerolinea']

    
    def validate_clase(self,clase):
        if clase == "":
            raise serializers.ValidationError('Debes seleccionar una Clase')
        return clase
    
    def validate_estado(self,estado): 
        if len(estado) < 2:
            raise serializers.ValidationError('Debe tener al menos 1 caracter')
        return estado
    
    def validate_incidencias(self,incidencias): 
        if len(incidencias) < 2:
            raise serializers.ValidationError('Debe tener al menos 1 caracter')
        return incidencias

    def validate_fecha_operacion(self, fecha_operacion):
        fechaHoy = datetime.datetime.now()

        if fechaHoy < fecha_operacion:
            raise serializers.ValidationError('La fecha de Opercion debe ser menor a Hoy')
        return fecha_operacion
    
    def validar_vuelo(self, vuelo):
        if len(vuelo) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos un vuelo')
        return vuelo
    
    def create(self, validated_data):
        aerolineas = self.initial_data("aerolinea")  # 🛠️ Extraer IDs de aerolíneas

        if len(aerolineas)<2:
            raise serializers.ValidationError({"aerolinea": ["Debe seleccionar al menos dos aerolínea"]})
        
        vuelo = Vuelo.objects.create(
            hora_salida = validated_data['hora_salida'],
            hora_llegada = validated_data['hora_llegada'],
            estado = validated_data['estado'],
            duracion = validated_data['duracion'],
            origen = validated_data['origen'],
            destino = validated_data['destino'],
            aerolinea = validated_data['aerolinea'],
        )
        vuelo.aerolinea.set(validated_data["aerolinea"])

        for aerolinea in aerolineas:
            modeloaerolinea = aerolinea.objects.get(id=aerolinea)
            Aerolinea.objects.create(aerolinea=modeloaerolinea,vuelo=vuelo)
        return vuelo
    
    def update(self, instance, validated_data):
        vuelos = self.initial_data.get("vuelo", [])  # 🛠️ Extrae IDs de vuelos
        aerolineas = self.initial_data.get("aerolinea", [])  # 🛠️ Extrae IDs de aerolíneas

        # ❌ Valida que al menos haya un vuelo y una aerolínea
        if len(vuelos) < 1:
            raise serializers.ValidationError(
                {'vuelo': ['Debe seleccionar al menos un vuelo']}
            )
        if len(aerolineas) < 1:
            raise serializers.ValidationError(
                {'aerolinea': ['Debe seleccionar al menos una aerolínea']}
            )

        # ✅ Actualiza los campos normales
        instance.fecha_operacion = validated_data.get("fecha_operacion", instance.fecha_operacion)
        instance.estado = validated_data.get("estado", instance.estado)
        instance.incidencias = validated_data.get("incidencias", instance.incidencias)
        instance.clase = validated_data.get("clase", instance.clase)
        instance.save()

        # ✅ Asigna relaciones ManyToMany correctamente
        instance.vuelo.set(vuelos)  # Asigna nuevos vuelos
        instance.aerolinea.set(aerolineas)  # Asigna nuevas aerolíneas

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
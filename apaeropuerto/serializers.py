from rest_framework import serializers
from .models import *
from .forms import *

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

    class Meta:
        fields = ('id',
                  'fecha_reserva',
                  'codigo_descueto',
                  'metodo_pago',
                  'estado_de_pago',
                  'pasajero',
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


class EstadisticasSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticasVuelo
        fields = '__all__'




class AeropuertoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Aeropuerto
        fields = '__all__'

        nombre = serializers.CharField()
        ciudad = serializers.ChoiceField(choices=Aeropuerto.CIUDADES)
        pais = serializers.ChoiceField(choices=Aeropuerto.PAISES)
        capacidad_maxima = serializers.IntegerField()

        def validate_nombre(self,nombre):
            nombre = Aeropuerto.objects.filter(nombre=nombre).first()

            if(not nombre is None):
                if(not self.instance is None and nombre.id == self.instance.id):
                    pass
                else:
                    raise serializers.ValidationError('Ya existe un Aeropuerto con ese nombre')

                if len(nombre) == "":
                    raise serializers.ValidationError('Al menos debes indicar 1 caracteres')            
            
            return nombre
        
        def validate_ciudad(self,ciudad):
            if len(ciudad) == "":
                raise serializers.ValidationError('Debes seleccionar una ciudad')
            return ciudad
        
        def validate_pais(self,pais):
            if len(pais) == "":
                raise serializers.ValidationError('Debes seleccionar un pais')
            return pais
        
        def validate_capacidad_max(self,capacidad_maxima):
            if len(capacidad_maxima) < 150:
                raise serializers.ValidationError('Debes tener una capacidad de 150 pasajeros')
            return capacidad_maxima
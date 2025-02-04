# De que va el trabajo => 7
# Tema Modelos => Linea 13
# Tema QuerySet = Linea 228
# Tema Templates => Linea 299
# Tema formularios CRUD => Linea 311


# entrega_de_trabajos
Mi pagina web va a consistir en un Aeropuerto en general con sus aerolineas que serian las distintas empresa como rayane, vueling ... ,
los vuelos que hay con sus pasajeros que seran las personas , los trabajadores que trabajen en el aeropuerto , el equipage que lleve una persona tambien las reservas de las personas , las ruta que deben tomar los aviones, y lod sitios del avion donde se sienta la gente.

sera una pagina donde se controlara toda la informacion de un aeropuerto 
-------------------------------------------------------------------------------------------------------------------------------------------

# Tema Modelos
Aeropuerto
    Atributos: 4
        Nombre (varchar ,maximo de caracteres 100, Definimos el nombre de la tabla admin)
        Ciudad (varchar ,maximo de caracteres 2, choices para que solo pueda elegir entre varias ciudades , por defecto que ponga ES)
        País (varchar , maximo de caracteres 2, choices para que solo pueda elegir entre varios paises , por defecto que ponga ES)
        capacidad maxima (Entero, este campo por defecto es 150 aviones)

        Funcion:
            str: para que en el admi aparezca el nombre

ContactoAeropuerto
    Atributos: 4
        nombre_contacto (varchar , maximo caracteres 100)
        telefono_contacto (varchar , maximo caracteres 100)
        email_contacto(email , se puede dejar en blanco)
        años_trabajado (Entero, el nombre se pone años trabajo , por defecto 0 años)
        
        Relacion: 
            Aeropuerto(OneToOne)

        Funcion: 
            str: Devuelve el nombre del contacto en el admin f para concadenar

Aerolinea
    Atributos: 4
        nombre (varchar de 100 caracterex max, nombre que mostrara en el formulario en vez de nombre aerolinea operadora)
        codigo (varchar, maximo 10 caracteres)
        fecha_fundacion (dia y hora , guarda automaticamente la fecha y hora al crear un registro)
        pais (varchar, maximo 2 caracteres , chices para que elija uno de los paises proporcionados, por defecto sera españa)

        Relacion : 1
            aerolinea(ManyToMany)
        
        Funcion: 
            str: Devuelve el nombre en el admin


Vuelo
    Atributos: 5
        hora_salida (dia y hora , no se puede dejar en blanco y sae un mensaje de error)
        hora_llegada (dia y hora , no se puede dejar en blanco y sae un mensaje de error)
        estado (si esta volando o no , nombre de la columna en la base de datos Volando)
        duracion(duracion , no se puede editar)

        Relacion:
            origen (ManyToOne)
            destino (ManyToOne)
            aerolinea (ManyToMany)

        Funcion:
            Clean => Verifica que el aeropuerto destino y origen no coincida
            save => calcula la duracion del vuelo

EstadisticasVuelo
    Atributos: 
        fecha_estadisticas (Dato , se pone automaticamente la fecha de creacion si no pones nada)
        numero_asientos_vendidos = (Entero, por defecto 0)
        numero_cancelaciones(Enteros , por defecto 0)
        feedback_pasajeros (varchar , se puede dejar en blanco)

        Relacion:
            Vuelo(OneToOne)


Pasajero
    Atributos: 5
        nombre (varchar,maximo 20 caracteres)
        apellido (varchar, maximo 20 caracteres, hacepta valores vacios)
        email (verifica el correo)
        telefono (Enteros , valida hasta 9 valores, puede ser un campo vacio)
        fecha de nacimiento (Dia y hora, puede ser nulo)

        Relacion:2
            Vuelo(ManyToMany)

        Funcion:
            str: muestra el nombre y apellido en el admin
            Valida si el dominio esta bien o no escrito y te pone un erro si no esta bien escrito

PerfilPasajero
    Atributos:
        direccion (varchar , maximo de caracteres 255, se puede dejar en blanco)
        documento_identidad (varchar , maximo de caracteres 9, es unico no puede a ver mas de uno)
        nacionalidad (varchar , maximo de caracteres 50, se puede dejar en blanco)
        vivienda (varchar , maximo de caracteres 50, se puede dejar en blanco)
        Relaciones:
            pasajero (OneToOne)

        Funcion
            str (muestra Dni en el admin)

Equipage
    Atributos: 4
        peso (decimales)
        dimensiones (varchar maximo 100 caracteres)
        tipo de material (varchar),maximo 100 caracteres
        color (varchar)

        Relacion: 2
            pasajero (ManyToOne)

        Funcion:
            str (muestra en el admi una cadena)


VueloAerolinea (Tabla intermedia)
    Atributos: 5
        fecha operacion(dia y hora, se puede poner nulo)
        esatdo (texto)
        clase(varchar , choices para elegir una clase)
        numero de aviones volando (Enteros,por defecto 5)
        insidencias (varchar , maximo caracteres 100)
        Relaciones: 2
            vuelo(ManyToOne)
            aerolinea(ManyToOne)

Reserva
    Atributo
        fecha de la reserva (por defecto es la fechqa de creacion)
        estado (varchar maximo 50 caracteres, introduce una ayuda)
        metodo de pago (varchar, choise para elegir metodo, por defecto targeta)
        codigo de descuento (varchar de 100 caracteres)

        Relacion
            pasajero(ManyToOne)
            vuelo(ManyToOne)

Asiento
    Atributos
        clase (varchar , maximo 1 caracter, choices para elegir la clase y por defecto Economico)
        precio (decimales, ,maximo 5 digitos, 2 decimales)
        posicion (varchar , maximo caracteres 1, choices para elegir la posicion)
        sistema_entretenimiento(hay tv o no)

        Relacion
            vuelo (Muchos a Uno)
            pasajero(Uno a Uno)

Servicio
    Atributos
        tipo de servicio (varchar , maximo 100 caracter)
        costo (decimales)
        duracion del servicio (tiempo)
        añadido del servicio (varchar, maximo 100 caracter)

        Relacion
            aeropuerto (ManyToMany)
        
        Fucnio:
            str (tipo de servicio que se muestra en el admi)

Empleado
    Atributo
        nombre (varchar, maximo 100 caracteres)
        apellido (varchar, maximo 100 caracteres)
        cargo (varchar,maximo 2 caracteres, choices para saber si es jefe o empleado)
        fecha_contratacion (dia y hora)

        Relacion
            Servicio(ManyToMany)
        
        Funcion:
           str: Devuelve nombre apellido y cargo la f es para concadenar  


Ruta
    Atributos:
        clima (varchar de 100)
        destino (varchar de 100)
        comentarios (varchar de 100)
        altura (Entero)

        Relacion:
            origen (muchos a muchos)
            destino (muchos a muchos)
            vuelo (muchos a muchos)



-------------------------------------------------------------------------------------------------------------------

# Modelos 

ManyToOne = Vuelo(origen) , Vuelo(destino) , Equipaje(pasajero) , Reserva(pasajero) , Reserva(Vuelo)
ManyToMany = Aerolínea(Aeropuerto) , Vuelo(Aerolinea) , Pasajero(vuelo)
OneToOne = ContactoAeropuerto(Aeropuerto) , EstadisticasVuelo(Vuelo), PerfilPasajero(pasajero)

# atributo

CharField, IntegerField, EmailField, DateField, DateTimeField,
BooleanField, DurationField, TextField, FloatField, DecimalField

# parametros

1. max_length = 100  => maximo de caracteres 100
2. verbose_name="Aeropuerto" => como se ve en el administrador en el formulario
3. choices=CIUDADES  =>  es para que solo pueda elejir una opcion del array
4. default='ES'  => por defecto poge ES si no pone nada
5. blank=True  => puede dejar el campo en blanco
6. auto_now_add=True  => si no pones nada pone la hora actual
7. error_messages={'blank': 'Este campo no puede estar vacío.',}  =>  pone un mensaje de error
8. db_column='Volando' => te cambia el nombre de la columna de la base de datos
9. editable=False  => no se puede editar en el admin
10. validators=[ MaxValueValidator(999999999)] => valida si el numero es menor al puesto
11. unique=True => el valor es unico
12. max_digits=6 => solo puede poner 6 dijitos contando con los dos de decimales
13. decimal_places=2 => solo puede poner 2 decimales.




-------------------------------------------------------------------------------------------------------------------

# Tema QuerySet:

Ejercicio 1. Todos los pasajeros que esten asociados a un vuelo con una relación reversa
desde la tabla vuelo cojo los datos y con el Prefetch hago la relacion inversa con el .get cojo el id expecifico de la tabla.


Ejercicio 2. Todos los vuelos que esten volando que esten una año en concreto.
    Template:
    En el titulo utilizo {{ datosvuelo.0.fecha_estadisticas |date:"Y" }} que el 0 es el primer elemento de la lista y con date:"y" me da solo el año pero eso hace que tenga otra queryset adicional si quitas el 0 del titulo se quita la queryset y se queda en una queryset aunque
    {{ datosvuelo.fecha_estadisticas |date:"Y" }} sin el 0 no te mostraria nada.
    (Importante: solo es para que lo vieras no me quites puntos por eso que solo lo he hecho en este ejercicio.)
    En la variable estado uso un if que dice si es true me imnprima vuelo si es false me imprima aterrizado.


Ejercicio 3. feedbacks de todos los vuelos que tenga una palabra en concreto de una aerolinea en concreto desde la tabla intermedia
    Cojo la aerolinea aparte en una variable para luego en la temple usarla sin bucle solo quiero una
    Con vuelo_aerolinea cojo todas las vuelos de ese erolinea y voy buscando el feedback_pasajeros de la tabla EstadisticasVuelo.


Ejercicio 4. Obtener el feedbacks de todos los vuelos en el que ha estado un pasajero específico.
    Primero obtengo al pasajero porque quiero mostrar solo uno.
    Cojo la tabla estadiscitas para recorrerla y vuelo para coger el id vuelo.

Ejercicio 5.Obtener todos los vuelos que salgan desde un aeropuerto específico y lleguen a un destino específico

Ejercicio 6. Listar reservas por método de pago y año

Ejercicio 7. Obtener todos los vuelos que tengan un origen y destino en concreto o que el estado sea volando
    Utilizo Q para las condiciones or y and y para la negacion ~Q.

Ejercicio 8. Calcular el peso total del equipaje de todos los pasajeros en un vuelo específico y ordenar
    Con el order_by y - delante del atributo ordenamo en descenso solo elijo los 5 primeros que me salgan con [:5].
    Con el aggregate podemos hacer operaciones de agragacion.
    sum se utiliza para sumar toda la lista pero tambien hay mas como:  promedio = Avg, 
                                                                        contar = Count,
                                                                        maximo y minimo = Max y Min
    aggregate te devuelve un diccionario con el resultado que en mi caso es esto = ['peso__sum'] 

Ejercicio 9. Listar todos los vuelos de una aerolínea específica que no tienen registrada una fecha de operación en la tabla intermedia
    Con el isnull=true hago que solo coja los nulos

Ejercicio 10. Calcular cuantos pasajeros hay en un vuelo
    Aqui uso count para contar



---------------------------------------------------------------------------------------------------------------------------
Usar al menos 5 templates tags diferentes: if-else, for..empty,en algunas páginas del proyecto. Indicar  cuales y donde en el README

    1.En casi todas las tamplates/paginas uso {% for %}
    2.En muchas paginas uso {% if %} por ejemplo => templates/Listas/Vuelo_Aerolinea.html
    3.En todas las templates/paginas uso {% include %}
    4.En todas las templates/paginas uso {% block %} y {% endblock %}
    5.En Principal uso {% static %}
    6.En el index uso {% url %} // para poner enlaces
    7.En Principal uso {% comment %}  {% endcomment %} // para poner comentarios
    8.En templates/consultas pasajeros_vuelo.html uso { forloop.counter } //contador


Usar al menos 5 operadores diferentes. Indicar cuales y dónde en el README

    1.En consultas/pasajero_vuelo hay un operador <
    2.En consultas/historial_feedbacks... hay un if else
    3.En consultas/pasajeros_vuelo hay un > el .count cuenta cuantos elementos hay
    4.En consultas/peso_equipaje_vuelo hay  =< => y un and
    5.En consultas/reservas por metodo de pago hay  == y or


Usa al menos 10 template filters en el proyecto

    1.En consultas/reservas => |lower  //pone la cadena en minuscula
    2.En Listas/Aerolinea => |date:"d-m-Y" //pone dia - mes - año
    3.En Listas/Vuelo_Aerolinea => default:"Sin valor"
    4.En Listas/Aerolinea => |upper //pone la cadena en mayusculas
    5.En Listas/Reservas => yesno:"Pagado,Pendiente de pago ,Sin datos" //para booleanos
    6.En Listas/Silla => |add:"55" //suma el valor a una variable
    7.En Listas/Pasajero => |capfirst // capitaliza solo la primera letra de una cadena, dejando las demás letras sin cambios
    8.En Listas/Estadisticas => |truncatechars:80 //la cadena solo puede tener maximo 80 caracteres
    9.En Listas/Aeropuerto => |title // pone en mayuscula la primera letra de cada palabra
    10.En Listas/Equipaje => |floatformat:2 // pone 2 numeros detras de la coma

---------------------------------------------------------------------------------------------------------------------------
# Tema formularios CRUD :

validaciones:
AeropuertoForm
nombre: Valida que no esté vacío y que no exista otro aeropuerto con el mismo nombre.
capacidad_maxima: Valida que no supere 150.

BusquedaAvanzadaAeropuertoForm
textoBusqueda: Valida que no esté vacío y que tenga al menos 1 carácter.

ContactoAeropuertoForm
nombre_contacto: Valida que no esté vacío.
telefono_contacto: Valida que tenga exactamente 9 dígitos.

BusquedaAvanzadaContacto
Campos generales: Al menos uno debe estar relleno.
años_trabajados: No puede ser menor a 0.

EstadisticasVueloForm
numero_cancelaciones: No puede superar el número de asientos vendidos.
numero_asientos_vendidos: Debe ser mayor a 0.

BusquedaAvanzadaEstadisticas
Campos generales: Al menos uno debe estar rellenado.
numero_asientos_vendidos y numero_cancelaciones: Valida que el número de asientos vendidos no sea menor que las cancelaciones.

AerolineaForm
nombre:Valida que no estén vacíos y que no exista otra aerolínea con el mismo nombre.
codigo_aerolinea: Valida que no estén vacíos y que no exista otra aerolínea con el mismo nombre.

BusquedaAvanzadaAerolinea
Campos generales: Al menos uno debe estar rellenado.
nombre: Debe tener al menos 3 caracteres.

VueloForm
origen y destino: No pueden ser iguales.
hora_llegada: Debe ser posterior a la hora de salida.

BusquedaAvanzadaVuelo
hora_salida y hora_llegada: Valida que la hora de salida no sea mayor que la hora de llegada.
origen y destino: No pueden ser iguales.

PasajeroForm
telefono: Debe tener exactamente 9 dígitos y contener solo números.
fecha_nacimiento: No puede ser futura ni mayor a 100 años en el pasado.

BusquedaAvanzadaPasajero
nombre: no puede estar vacio.
telefono: Debe tener exactamente 9 dígitos.




widgets usados:

2.maxlength: Límite máximo de caracteres.
3.min: Definen el rango de valores minimo.
4.max: Definen el rango de valores maximo.
5.class: Define la clase CSS para estilizar el elemento.
6.date:  usar el selector de fechas del navegador.
7.datetime-local:  para permitir la selección combinada de fecha y hora.


---------------------------------------------------------------------------------------------------------------------------
# Tema Sesiones y Autenticacion :

* En nuestra aplicación debemos incluir al menos dos tipos de usuarios claramente diferenciados(No cuenta el usuario administrador) (1 puntos).

* En cada vista controlarse los permisos y si el usuario esta logueado o no (1 punto).

* En cada template de vista y formulario controlarse los permisos y si el usuario esta logueado o no (1 punto).

* Incluir al menos 4 variables que se guarden en la sesión y que aparezcan siempre en la cabacera de la página. Y se eliminen cuando se desloguea el usuario. (1 punto).

Debemos hacer un registro de los distintos tipos de usuario, salvo el administrador, con sus validaciones correspondiente, y controlar que dependiendo del tipo de usuario tendrá unos valores u otros (1 punto).

* Debemos hacer un login y logout del usuario (1 punto).

Debe crearse una funcionalidad en algún formulario , que el contenido de algún select ManyToMany o ManyToOne varie dependiendo del usuario que está logueado. (1 punto).

* En los formularios de crear debe incluirse siempre el usuario que crea dicho registro por la sesión del usuario. (1 punto)
Debe crearse una funcionalidad en algún formulario de búsqueda , que el contenido se filtre por el suario que está logueado. (1 punto).

Implementar funcionalidad de reinicio de contraseña.  Ten en cuenta que tu aplicación en local no permite el envó de email, pero hay una forma en Django para obtener dicho enlace de recuperación de contraseña. Investiga! (1 punto)


# Tipos de usuarios:

* ESta el usuario Pasajero que puede hacer reservas del vuelo siempre que reserve sera con su id y si busca la reserva solo se mostrara su id.

Esta el usuario gerente que debe poder hace las estadisticas de vuelo.


---------------------------------------------------------------------------------------------------------------------------
# comandos :

python3 -m venv myvenv
source myvenv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations apaeropuerto
python manage.py migrate apaeropuerto
python manage.py seed apaeropuerto --number=20
python manage.py dumpdata --indent 4 > apaeropuerto/fixtures/datos_sesion.json
python manage.py loaddata apaeropuerto/fixtures/datos2.json

python manage.py createsuperuser
python manage.py runserver


git add .
git commit -m 'Completado'
git push
git pull

#para el servidor
python manage.py runserver 127.0.0.1:8081

-----------------------------------------------------------------------------------
from django.db.models import Prefetch

# Aeropuerto
Aeropuerto.objects.prefetch_related(
    Prefetch('aerolinea_de_aeropuerto'),  # ManyToMany con Aerolínea
    Prefetch('vuelos_de_origen'),         # ManyToOne reversa con Vuelo (origen)
    Prefetch('vuelos_de_destino'),        # ManyToOne reversa con Vuelo (destino)
    Prefetch('servicio_aeropuerto')       # ManyToMany con Servicio
)

# ContactoAeropuerto
ContactoAeropuerto.objects.select_related(
    'aeropuerto'                          # OneToOne con Aeropuerto
)

# Aerolínea
Aerolinea.objects.prefetch_related(
    Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
    Prefetch('vuelo_aerolinea')           # ManyToMany con Vuelo
)

# Vuelo
Vuelo.objects.prefetch_related(
    Prefetch('vuelo_pasajero'),           # ManyToMany con Pasajero
    Prefetch('asiento_vuelo'),            # ManyToOne con Asiento
    Prefetch('vuelo_reserva'),            # ManyToOne con Reserva
    Prefetch('vuelo_media_aerolinea'),    # ManyToOne con VueloAerolinea
    Prefetch('vuelo_datos')               # OneToOne con EstadisticasVuelo
).select_related(
    'origen',                             # ManyToOne con Aeropuerto (origen)
    'destino'                             # ManyToOne con Aeropuerto (destino)
)

# EstadisticasVuelo
EstadisticasVuelo.objects.select_related(
    'vuelo'                               # OneToOne con Vuelo
)

# Pasajero
Pasajero.objects.prefetch_related(
    Prefetch('vuelo_pasajero'),           # ManyToMany con Vuelo
    Prefetch('equipaje_pasajero'),        # ManyToOne con Equipaje
    Prefetch('reserva_pasajero'),         # ManyToOne con Reserva
    Prefetch('pajarelo_asiento'),         # ManyToOne con Asiento
    Prefetch('pasajero_datos')            # OneToOne con PerfilPasajero
)

# PerfilPasajero
PerfilPasajero.objects.select_related(
    'pasajero'                            # OneToOne con Pasajero
)

# Equipaje
Equipaje.objects.select_related(
    'pasajero'                            # ManyToOne con Pasajero
)

# Reserva
Reserva.objects.select_related(
    'pasajero',                           # ManyToOne con Pasajero
    'vuelo'                               # ManyToOne con Vuelo
)

# Asiento
Asiento.objects.select_related(
    'vuelo',                              # ManyToOne con Vuelo
    'pasajero'                            # ManyToOne con Pasajero
)

# Servicio
Servicio.objects.prefetch_related(
    Prefetch('aeropuerto'),               # ManyToMany con Aeropuerto
    Prefetch('empleado_servicio')         # ManyToOne con Empleado
)

# Empleado
Empleado.objects.select_related(
    'servicio'                            # ManyToOne con Servicio
)


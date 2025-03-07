# Generated by Django 5.1.5 on 2025-01-20 12:56

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeropuerto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Aeropuerto')),
                ('ciudades', models.CharField(choices=[('ES', 'Madrid'), ('FR', 'París'), ('IT', 'Roma'), ('DE', 'Berlín'), ('PT', 'Lisboa'), ('NL', 'Ámsterdam'), ('BE', 'Bruselas'), ('SE', 'Estocolmo'), ('AT', 'Viena'), ('CH', 'Ginebra')], default='ES', max_length=2)),
                ('pais', models.CharField(choices=[('ES', 'España'), ('FR', 'Francia'), ('IT', 'Italia'), ('DE', 'Alemania'), ('PT', 'Portugal'), ('NL', 'Países Bajos'), ('BE', 'Bélgica'), ('SE', 'Suecia'), ('AT', 'Austria'), ('CH', 'Suiza')], default='ES', max_length=2)),
                ('capacidad_maxima', models.IntegerField(default=150)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'administardor'), (2, 'pasajero'), (3, 'empleado')], default=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aerolinea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Aerolínea operadora')),
                ('codigo', models.CharField(max_length=10)),
                ('fecha_fundacion', models.DateField(auto_now_add=True)),
                ('pais', models.CharField(choices=[('ES', 'España'), ('EN', 'Inglaterra'), ('FR', 'Francia'), ('IT', 'Italia')], default='ES', max_length=2)),
                ('aeropuerto', models.ManyToManyField(related_name='aerolinea_de_aeropuerto', to='apaeropuerto.aeropuerto')),
            ],
        ),
        migrations.CreateModel(
            name='ContactoAeropuerto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_contacto', models.CharField(max_length=100)),
                ('telefono_contacto', models.CharField(blank=True, max_length=15)),
                ('email_contacto', models.EmailField(blank=True, max_length=254)),
                ('años_trabajados', models.IntegerField(default=0, verbose_name='Años Trabajado')),
                ('aeropuerto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apaeropuerto.aeropuerto')),
            ],
        ),
        migrations.CreateModel(
            name='Gerente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=9)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField()),
                ('dimensiones', models.CharField(max_length=50)),
                ('tipo_material', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=50)),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipaje_pasajero', to='apaeropuerto.pasajero')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reserva', models.DateTimeField(default=django.utils.timezone.now)),
                ('codigo_descueto', models.CharField(max_length=100)),
                ('metodo_pago', models.CharField(choices=[('tarjeta', 'Tarjeta de crédito'), ('efectivo', 'Efectivo'), ('paypal', 'PayPal')], default='tarjeta', max_length=10)),
                ('estado_de_pago', models.BooleanField(default=False)),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_pasajero', to='apaeropuerto.pasajero')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servicio', models.CharField(max_length=100)),
                ('costo', models.FloatField()),
                ('duracion_servicio', models.TimeField()),
                ('añadido', models.CharField(max_length=100)),
                ('aeropuerto', models.ManyToManyField(related_name='servicio_aeropuerto', to='apaeropuerto.aeropuerto')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('cargo', models.CharField(choices=[('JE', 'Jefe'), ('EM', 'Empleado')], default='EM', max_length=2)),
                ('fecha_contratacion', models.DateField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_servicio', to='apaeropuerto.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Vuelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_salida', models.DateTimeField(error_messages={'blank': 'Este campo no puede estar vacío.'})),
                ('hora_llegada', models.DateTimeField(error_messages={'blank': 'Este campo no puede estar vacío.'})),
                ('estado', models.BooleanField(db_column='Volando')),
                ('duracion', models.DurationField(editable=False)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vuelos_de_destino', to='apaeropuerto.aeropuerto')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vuelos_de_origen', to='apaeropuerto.aeropuerto')),
            ],
        ),
        migrations.AddField(
            model_name='pasajero',
            name='vuelo',
            field=models.ManyToManyField(related_name='vuelo_pasajero', to='apaeropuerto.vuelo'),
        ),
        migrations.CreateModel(
            name='EstadisticasVuelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_estadisticas', models.DateField(auto_now_add=True)),
                ('numero_asientos_vendidos', models.IntegerField(default=0)),
                ('numero_cancelaciones', models.IntegerField(default=0)),
                ('feedback_pasajeros', models.TextField(blank=True)),
                ('vuelo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vuelo_datos', to='apaeropuerto.vuelo')),
            ],
        ),
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.CharField(choices=[('E', 'Economy'), ('B', 'Business'), ('F', 'First Class'), ('P', 'Premium Economy'), ('L', 'Luxury'), ('S', 'Standard'), ('H', 'Hybrid'), ('X', 'Extra Legroom'), ('R', 'Regional'), ('C', 'Charter')], default='E', max_length=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('posicion', models.CharField(choices=[('P', 'Pasillo'), ('M', 'Medio'), ('V', 'Ventana')], max_length=1)),
                ('sistema_entretenimiento', models.BooleanField()),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pajarelo_asiento', to='apaeropuerto.pasajero')),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asiento_vuelo', to='apaeropuerto.vuelo')),
            ],
        ),
        migrations.CreateModel(
            name='VueloAerolinea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_operacion', models.DateTimeField(blank=True, null=True)),
                ('estado', models.TextField()),
                ('clase', models.CharField(choices=[('E', 'Economy'), ('B', 'Business'), ('F', 'First Class'), ('P', 'Premium Economy'), ('L', 'Luxury'), ('S', 'Standard'), ('H', 'Hybrid'), ('X', 'Extra Legroom'), ('R', 'Regional'), ('C', 'Charter')], default='E', max_length=1)),
                ('incidencias', models.CharField(max_length=100)),
                ('aerolinea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aerolinea_media_aerolinea', to='apaeropuerto.aerolinea')),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vuelo_media_aerolinea', to='apaeropuerto.vuelo')),
            ],
        ),
        migrations.AddField(
            model_name='vuelo',
            name='aerolinea',
            field=models.ManyToManyField(related_name='vuelo_aerolinea', through='apaeropuerto.VueloAerolinea', to='apaeropuerto.aerolinea'),
        ),
    ]

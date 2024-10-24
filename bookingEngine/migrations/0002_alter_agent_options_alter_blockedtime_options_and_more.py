# Generated by Django 5.1 on 2024-10-24 01:22

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingEngine', '0001_initial'),
        ('marketplace', '0016_company_facebook_url_company_google_maps_url_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'verbose_name': 'Agente', 'verbose_name_plural': 'Agentes'},
        ),
        migrations.AlterModelOptions(
            name='blockedtime',
            options={'verbose_name': 'Tiempo Bloqueado', 'verbose_name_plural': 'Tiempos Bloqueados'},
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-start_datetime'], 'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name': 'Recurso', 'verbose_name_plural': 'Recursos'},
        ),
        migrations.AlterModelOptions(
            name='resourcetype',
            options={'verbose_name': 'Tipo de Recurso', 'verbose_name_plural': 'Tipos de Recursos'},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Horario', 'verbose_name_plural': 'Horarios'},
        ),
        migrations.AlterField(
            model_name='agent',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(help_text='Correo electrónico de contacto del agente', max_length=254, verbose_name='Correo electrónico'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Indica si el agente está activo y puede recibir reservas', verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(help_text='Nombre completo del agente', max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='phone',
            field=models.CharField(help_text='Número de teléfono del agente', max_length=20, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(blank=True, help_text='Usuario del sistema asociado al agente', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='agent',
            field=models.ForeignKey(blank=True, help_text='Agente que estará bloqueado', null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.agent', verbose_name='Agente'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='end_datetime',
            field=models.DateTimeField(help_text='Fin del período bloqueado', verbose_name='Fecha y hora de fin'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='reason',
            field=models.TextField(help_text='Motivo por el cual se bloquea este período', verbose_name='Motivo'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='resource',
            field=models.ForeignKey(blank=True, help_text='Recurso que estará bloqueado', null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.resource', verbose_name='Recurso'),
        ),
        migrations.AlterField(
            model_name='blockedtime',
            name='start_datetime',
            field=models.DateTimeField(help_text='Inicio del período bloqueado', verbose_name='Fecha y hora de inicio'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='agent',
            field=models.ForeignKey(blank=True, help_text='Agente asignado a la reserva (si aplica)', null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.agent', verbose_name='Agente'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_datetime',
            field=models.DateTimeField(help_text='Fecha y hora de finalización de la reserva', verbose_name='Fecha y hora de fin'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='notes',
            field=models.TextField(blank=True, help_text='Notas adicionales sobre la reserva', verbose_name='Notas'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='resource',
            field=models.ForeignKey(help_text='Recurso que se está reservando', on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.resource', verbose_name='Recurso'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_datetime',
            field=models.DateTimeField(help_text='Fecha y hora de inicio de la reserva', verbose_name='Fecha y hora de inicio'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmada'), ('cancelled', 'Cancelada'), ('completed', 'Completada')], default='pending', help_text='Estado actual de la reserva', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Última actualización'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(help_text='Usuario que realiza la reserva', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='advance_booking_limit',
            field=models.IntegerField(default=30, help_text='Número máximo de días con anticipación que se permite realizar una reserva', verbose_name='Límite de anticipación'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='automatic_confirmation',
            field=models.BooleanField(default=False, help_text='Las reservas se confirmarán automáticamente sin requerir aprobación manual', verbose_name='Confirmación automática'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='cancellation_limit_hours',
            field=models.IntegerField(default=24, help_text='Horas límite antes de la reserva para permitir cancelaciones', verbose_name='Límite de cancelación'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='company',
            field=models.ForeignKey(help_text='Empresa a la que pertenece esta configuración', on_delete=django.db.models.deletion.CASCADE, to='marketplace.company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='google_calendar_credentials',
            field=models.JSONField(blank=True, help_text='Credenciales de autenticación para Google Calendar', null=True, verbose_name='Credenciales de Google Calendar'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='google_calendar_enabled',
            field=models.BooleanField(default=False, help_text='Habilita la sincronización con Google Calendar', verbose_name='Google Calendar activado'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='notification_email',
            field=models.EmailField(blank=True, help_text='Correo electrónico para recibir notificaciones del sistema', max_length=254, null=True, verbose_name='Email de notificaciones'),
        ),
        migrations.AlterField(
            model_name='bookingsettings',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Última actualización'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='agents',
            field=models.ManyToManyField(blank=True, help_text='Agentes que pueden atender este recurso', related_name='resources', to='bookingEngine.agent', verbose_name='Agentes'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='availability_type',
            field=models.CharField(choices=[('always', 'Siempre disponible'), ('schedule', 'Según horario'), ('custom', 'Personalizado')], default='schedule', help_text='Define cómo se maneja la disponibilidad del recurso', max_length=20, verbose_name='Tipo de disponibilidad'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(help_text='Descripción detallada del recurso', verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='duration',
            field=models.IntegerField(help_text='Duración en minutos de la reserva', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Duración'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Indica si el recurso está activo y puede ser reservado', verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(help_text='Nombre del recurso', max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Precio del recurso (opcional)', max_digits=10, null=True, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.resourcetype', verbose_name='Tipo de recurso'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='description',
            field=models.TextField(help_text='Descripción detallada del tipo de recurso', verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='name',
            field=models.CharField(help_text='Nombre del tipo de recurso (ej: Servicio, Habitación, Mesa)', max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='requires_agent',
            field=models.BooleanField(default=True, help_text='Indica si este tipo de recurso necesita un agente para ser reservado', verbose_name='Requiere agente'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='agent',
            field=models.ForeignKey(blank=True, help_text='Agente al que aplica este horario', null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.agent', verbose_name='Agente'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day_of_week',
            field=models.IntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')], help_text='Día de la semana para este horario', verbose_name='Día de la semana'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.TimeField(help_text='Hora de finalización del horario', verbose_name='Hora de fin'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='resource',
            field=models.ForeignKey(blank=True, help_text='Recurso al que aplica este horario', null=True, on_delete=django.db.models.deletion.CASCADE, to='bookingEngine.resource', verbose_name='Recurso'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(help_text='Hora de inicio del horario', verbose_name='Hora de inicio'),
        ),
    ]

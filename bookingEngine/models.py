# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

class BookingSettings(models.Model):
    company = models.ForeignKey(
        'marketplace.Company',
        on_delete=models.CASCADE,
        verbose_name='Empresa',
        help_text='Empresa a la que pertenece esta configuración'
    )
    google_calendar_enabled = models.BooleanField(
        default=False,
        verbose_name='Google Calendar activado',
        help_text='Habilita la sincronización con Google Calendar'
    )
    google_calendar_credentials = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Credenciales de Google Calendar',
        help_text='Credenciales de autenticación para Google Calendar'
    )
    notification_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email de notificaciones',
        help_text='Correo electrónico para recibir notificaciones del sistema'
    )
    advance_booking_limit = models.IntegerField(
        default=30,
        verbose_name='Límite de anticipación',
        help_text="Número máximo de días con anticipación que se permite realizar una reserva"
    )
    cancellation_limit_hours = models.IntegerField(
        default=24,
        verbose_name='Límite de cancelación',
        help_text="Horas límite antes de la reserva para permitir cancelaciones"
    )
    automatic_confirmation = models.BooleanField(
        default=False,
        verbose_name='Confirmación automática',
        help_text="Las reservas se confirmarán automáticamente sin requerir aprobación manual"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = "Configuración de Reservas"
        verbose_name_plural = "Configuraciones de Reservas"

class ResourceType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre del tipo de recurso (ej: Servicio, Habitación, Mesa)'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del tipo de recurso'
    )
    company = models.ForeignKey(
        'marketplace.Company',
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    requires_agent = models.BooleanField(
        default=True,
        verbose_name='Requiere agente',
        help_text="Indica si este tipo de recurso necesita un agente para ser reservado"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = "Tipo de Recurso"
        verbose_name_plural = "Tipos de Recursos"

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Agent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Usuario',
        help_text='Usuario del sistema asociado al agente'
    )
    company = models.ForeignKey(
        'marketplace.Company',
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre completo del agente'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico',
        help_text='Correo electrónico de contacto del agente'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        help_text='Número de teléfono del agente'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el agente está activo y puede recibir reservas'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"
        unique_together = ['company', 'email']

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Resource(models.Model):
    AVAILABILITY_CHOICES = [
        ('always', 'Siempre disponible'),
        ('schedule', 'Según horario'),
        ('custom', 'Personalizado'),
    ]
    
    type = models.ForeignKey(
        ResourceType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de recurso'
    )
    company = models.ForeignKey(
        'marketplace.Company',
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre del recurso'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del recurso'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio',
        help_text='Precio del recurso (opcional)'
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Duración',
        help_text="Duración en minutos de la reserva"
    )
    availability_type = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='schedule',
        verbose_name='Tipo de disponibilidad',
        help_text='Define cómo se maneja la disponibilidad del recurso'
    )
    agents = models.ManyToManyField(
        Agent,
        related_name='resources',
        blank=True,
        verbose_name='Agentes',
        help_text='Agentes que pueden atender este recurso'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el recurso está activo y puede ser reservado'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"

    def __str__(self):
        return f"{self.name} - {self.company.name}"

# models.py (continuación)

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Recurso',
        help_text='Recurso al que aplica este horario'
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Agente',
        help_text='Agente al que aplica este horario'
    )
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        verbose_name='Día de la semana',
        help_text='Día de la semana para este horario'
    )
    start_time = models.TimeField(
        verbose_name='Hora de inicio',
        help_text='Hora de inicio del horario'
    )
    end_time = models.TimeField(
        verbose_name='Hora de fin',
        help_text='Hora de finalización del horario'
    )

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        unique_together = [
            ['resource', 'day_of_week'],
            ['agent', 'day_of_week']
        ]

    def clean(self):
        if not self.resource and not self.agent:
            raise ValidationError('Debe especificar un recurso o un agente')
        if self.resource and self.agent:
            raise ValidationError('No puede especificar ambos: recurso y agente')
        if self.start_time >= self.end_time:
            raise ValidationError('La hora de inicio debe ser anterior a la hora de fin')

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        help_text='Usuario que realiza la reserva'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Recurso',
        help_text='Recurso que se está reservando'
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Agente',
        help_text='Agente asignado a la reserva (si aplica)'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Fecha y hora de inicio',
        help_text='Fecha y hora de inicio de la reserva'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Fecha y hora de fin',
        help_text='Fecha y hora de finalización de la reserva'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado',
        help_text='Estado actual de la reserva'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre la reserva'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-start_datetime']

class BlockedTime(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Recurso',
        help_text='Recurso que estará bloqueado'
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Agente',
        help_text='Agente que estará bloqueado'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Fecha y hora de inicio',
        help_text='Inicio del período bloqueado'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Fecha y hora de fin',
        help_text='Fin del período bloqueado'
    )
    reason = models.TextField(
        verbose_name='Motivo',
        help_text='Motivo por el cual se bloquea este período'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = "Tiempo Bloqueado"
        verbose_name_plural = "Tiempos Bloqueados"